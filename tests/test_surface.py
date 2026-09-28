from pathlib import Path
ROOT=Path(__file__).parents[1];SOURCE=(ROOT/'contracts'/'contract.py').read_text(encoding='utf-8')
def test_contract_surface():
 assert SOURCE.startswith('# { "Depends": "py-genlayer:')
 assert 'class CipherOrchard(gl.Contract):' in SOURCE
 for name in ('plant_specimen','propose_graft','get_specimen','get_grafts_page','get_specimens_page'):assert f'def {name}' in SOURCE
 assert 'run_nondet_unsafe' in SOURCE and 'emit_transfer' not in SOURCE
def test_required_documents():
 for name in ('PRODUCT_BOUNDARY.md','frontend-design-contract.md','readme-design-contract.md','README.md','VERIFICATION.md'):assert (ROOT/name).exists()
