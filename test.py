from tqdm import tqdm
from symbol import SymbolDB


def main():
    dbpath = "output/mathlib4_dependency_graph/symbol_5e932f97dd25535344f80f9dd8da3aab83df0fe6.db"
    with SymbolDB(dbpath) as kv:
        # print all kinds
        kinds = set()
        for symbol in tqdm(kv, total=len(kv), desc="getting all kinds ..."):
            kinds.add(symbol.kind)
        
        print(kinds)


        return
        # verify our db
        missing_name_set = set()
        for symbol in tqdm(kv, total=len(kv), desc="verifying db ..."):
            references = set(symbol.typeReferences + symbol.valueReferences)
            for name in references:
                if name not in kv:
                    if name not in missing_name_set:
                        missing_name_set.add(name)
                        print(len(missing_name_set), name)
    
        print(missing_name_set)



if __name__ == "__main__":
    main()
