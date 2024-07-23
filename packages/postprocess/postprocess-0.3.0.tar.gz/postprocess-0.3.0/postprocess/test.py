from typing import Optional, Tuple, Dict, List, Any
from enum import Enum, unique
from dataclasses import dataclass
from collections import deque
from rdkit import Chem
import json
import re
from rdkit.Chem.rdchem import Mol
from loguru import logger
LONG_CHAR_ELEMENTS = (
  'Cl', 'Br', 'Si', 'Na', 'Al', 'Ca', 'Sn', 'As', 
  'Hg', 'Fe', 'Zn', 'Cr', 'Se', 'Gd', 'Au', 'Li',
)

@dataclass
class Error:
    title: str
    msg: str
    
@dataclass
class PostProcessResult:
    model_mol: str = ''   # molecule representation for model 
    drawer_mol: str = ''  # molecule representation for drawer
    smi: str = ''         # SMILES display for user
    svg: str = ''         # reconstructed structure
    error: Optional[Error] = None

@unique
class TextType(Enum):
    SYMBOL = 'symbol'
    SCRIPT = 'script'
    MULTIPLE = 'multiple'
    PRIME = 'prime'

class Tokens:
    atom_start = '<a>'
    atom_end = '</a>'
    circ_start = '<c>'
    circ_end = '</c>'
    ring_start = '<r>'
    ring_end = '</r>'
    dummy = '<dum>'
    separator = '<sep>'
    long_char_elements_pattern = re.compile(rf'{"|".join(LONG_CHAR_ELEMENTS) + "|."}') 
    grp_content = re.compile(
        rf'(?P<{TextType.SYMBOL.value}>[A-Za-z0-9]*)' +
        rf'(?P<{TextType.SCRIPT.value}>(\[\S+\])?)' +
        rf'(?P<{TextType.PRIME.value}>[\'\"]?)' +
        rf'(?P<{TextType.MULTIPLE.value}>(\?([a-z]|\d{1}|\d-\d)$)?)'  # $ for matching string ending
    )
    grp_pattern = re.compile(
        rf'({atom_start}|{circ_start}|{ring_start}|{ring_start}{circ_start})' +
        rf'(\d+:\S+?)' +
        rf'({atom_end}|{circ_end}|{ring_end})'
    )

def strip_cxsmiles(cxsmi: str) -> Optional[str]:
    # A valid CXSMILES: '*c1nc(O)c2cc(Cl)ncc2n1 |$*;;;;;;;;;;;;$|'
    if cxsmi == '':  # deal with initial callback
        return
    items = cxsmi.split(' ')
    if len(items) > 2:
        logger.error(f'Invalid SMILES or CXSMILES: {cxsmi}')
        return
    return items[0]
 
def get_ring_mapping(
    tgt_mol: Mol,
    atom_mapping: Dict[int, int],  # target -> source
) -> Optional[Dict[int, int]]:
    """Find the mapping from source ring index to target ring index."""
    ring_info = tgt_mol.GetRingInfo()
    if ring_info.NumRings() == 0:
        return
    
    # First reorder rings in target molecule.
    tgt_rings: List[List[Tuple[int]]] = []
    for ring_atoms in ring_info.AtomRings():
        min_atom_idx = 1_000_000
        total_atom_idx = 0
        for atom_idx in ring_atoms:
            min_atom_idx = min(min_atom_idx, atom_idx)
            total_atom_idx += atom_idx
        tgt_rings.append(
            [(min_atom_idx, total_atom_idx / len(ring_atoms)), ring_atoms]
        )

    # Rank ring indices in target molecule.
    tgt_rings.sort(key=lambda x: (x[0][0], x[0][1]))
    src_rings = []
    for ri, (_, tgt_ring_atoms) in enumerate(tgt_rings):
        src_ring_atoms = tuple(atom_mapping[i] for i in tgt_ring_atoms)
        min_atom_idx = 1_000_000
        total_atom_idx = 0
        for atom_idx in src_ring_atoms:
            min_atom_idx = min(min_atom_idx, atom_idx)
            total_atom_idx += atom_idx
        src_rings.append({
            'tgt_idx': ri,
            'for_rank': (min_atom_idx, total_atom_idx / len(src_ring_atoms)), 
        })
        
    # Rank ring indices in source molecule.    
    src_rings.sort(key=lambda x: (x['for_rank'][0], x['for_rank'][1]))
    # source -> target
    return {src: item['tgt_idx'] for src, item in enumerate(src_rings)}

def load_extra(obj: str) -> List[Dict[str, Any]]:
    try:
        return json.loads(obj)['extra']  # List[Dict]
    except:
        if len(obj) > 0:
            logger.error(f'Invalid extra information: {obj}')
        return []
    
def get_mapped_groups(
        groups: List[Dict[str, Any]],
        atom_mapping: Dict[int, int],
        ring_mapping: Optional[Dict[int, int]] = None,
    ) -> List[Dict[str, Any]]:
        """Get groups after atom/ring index mapping."""
        atom_groups = []
        ring_groups = []
        
        for grp in filter(lambda x: x.get('idxType') == 'atom', groups):
            mapped_idx = atom_mapping.get(grp['idx'])
            if mapped_idx is not None:
                mapped_grp = grp.copy()
                mapped_grp['idx'] = mapped_idx
                atom_groups.append(mapped_grp)
        
        if ring_mapping is not None:
            for grp in filter(lambda x: x.get('idxType') == 'ring', groups):
                mapped_idx = ring_mapping.get(grp['idx'])
                if mapped_idx is not None:
                    mapped_grp = grp.copy()
                    mapped_grp['idx'] = mapped_idx
                    ring_groups.append(mapped_grp)
        
        # NOTE Keep new groups in ascending order.
        atom_groups.sort(key=lambda x: x['idx'])
        ring_groups.sort(key=lambda x: x['idx'])
        return atom_groups + ring_groups
    
class MoleculePostProcessor:
    def __init__(self) -> None:
        self._m1: Optional[Mol] = None
        self._m2: Optional[Mol] = None

    def _get_atom_matching(
        self, 
        smi: str, 
        block: str
    ) -> Tuple[Optional[Tuple[int, ...]], Optional[Error]]:
        # NOTE Do not touch parsed SMILES even if it is not canonical.
        self._m1 = Chem.MolFromSmiles(smi)
        self._m2 = Chem.MolFromMolBlock(block)
        if self._m1 is None or self._m2 is None:
            error = Error(title='Postprocess Error', msg='Failed to initialize molecule')
            return None, error
        
        match = self._m1.GetSubstructMatch(self._m2)  # Tuple[int, ...]
        # https://www.rdkit.org/docs/source/rdkit.Chem.rdchem.html#rdkit.Chem.rdchem.Mol.GetSubstructMatch
        # NOTE `match` holds the atom mapping between `m1` and `m2`, for example:
        # match = (0, 12, 2, 11, 10, 9, 7, 8, 5, 6, 3, 4, 1)
        # Then the atom mapping can be deduced as below
        # m1 | 0 | 12 | 2 | 11 | 10 | 9 | 7 | 8 | 5 | 6 | 3  | 4  | 1  |
        # m2 | 0 | 1  | 2 | 3  | 4  | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
        if len(match) == 0:
            logger.error(f'Atom mismatch between {smi} and {block}')
            error = Error(title='Postprocess Error', msg='Atom mismatch between SMILES and block')
            return None, error
        
        return match, None

    def _build_model_molecule(
        self,
        smi: str,
        groups: List[Dict[str, Any]],
    ) -> str:
        extra = ''
        for grp in groups:
            idx_type = grp.get('idxType')
            symbol = grp.get('symbol')
            script = grp.get('script')
            prime = grp.get('prime')
            multiple = grp.get('multiple')
            if idx_type not in ('atom', 'ring') or symbol is None:
                logger.error(f'Invalid group: {grp}')
                continue
            grp_repr = deque([str(grp['idx']), ':', str(symbol)])
            if script is not None:
                grp_repr.extend(['[', script, ']'])
            if prime is not None:
                grp_repr.append(prime)
            if multiple is not None:
                grp_repr.extend(['?', multiple])
            # Don't to forget to add group index.
            if idx_type == 'atom':
                grp_repr.appendleft(Tokens.atom_start)
                grp_repr.append(Tokens.atom_end)
            elif idx_type == 'ring':
                grp_repr.appendleft(Tokens.ring_start)
                grp_repr.append(Tokens.ring_end)
            extra += ''.join(grp_repr)
            
        return smi + Tokens.separator + extra

    def run(self, struct: str):
        if struct is None or struct == '':
            error_msg = 'Received empty structure'
            logger.error(error_msg)
            return PostProcessResult(
                error=Error(title='Postprocess Error', msg=error_msg)
            )
        
        items = struct.split(Tokens.separator)
        if len(items) != 3:
            logger.error(f'Invalid structure: {struct}')
            return PostProcessResult(
                error=Error(title='Postprocess Error', msg='Received invalid structure')
            )
            
        # 1) `cxsmi`: SMILES or CXSMILES NOTE atoms might be reordered after editing!
        # 2) `extra`: extra group info in JSON which keeps original atom order
        # 3) `block`: molecule structure block which keeps original atom order
        cxsmi, extra, block = items
        smi = strip_cxsmiles(cxsmi)
        if smi is None:
            return PostProcessResult(
                error=Error(title='Postprocess Error', msg=f'Failed to strip SMILES from {cxsmi}')
            )
                    
        match, error = self._get_atom_matching(smi, block)
        if error is not None:
            return PostProcessResult(error=error)
        
        # Align atom/ring indices.
        groups = load_extra(extra)
        new_groups = []
        if len(groups) > 0:
            ring_mapping = get_ring_mapping(
                tgt_mol=self._m1, 
                atom_mapping={j: i for i, j in enumerate(match)},  # from `m1` to `m2`
            )
            new_groups = get_mapped_groups(
                groups=groups,
                atom_mapping={i: j for i, j in enumerate(match)},
                ring_mapping=ring_mapping,
            )
        
        model_mol = self._build_model_molecule(smi, groups=new_groups)
        return model_mol
        
        
        