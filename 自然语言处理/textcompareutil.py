from difflib import Differ

a="17.3如发包方有证据认为承包方无法完全履行本合同而承包方无法提供有效的担保时,"
b="173如发包方有证虽“为采包方无法完全用行木合同而承包方无法提供有效的担保时"

d = Differ()
diff = d.compare(a.splitlines(), b.splitlines())
print('\n'.join(list(diff)))