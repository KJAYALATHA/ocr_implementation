import enchant

def correct_spelling(address_text):
    # Load English dictionary
    d = enchant.Dict("en_US")
    
    # Tokenize the address text
    tokens = address_text.split()
    
    # Correct spelling for each token
    corrected_tokens = []
    for token in tokens:
        if not d.check(token):
            suggestions = d.suggest(token)
            if suggestions:
                corrected_tokens.append(suggestions[0])
            else:
                corrected_tokens.append(token)
        else:
            corrected_tokens.append(token)
    
    # Reconstruct the corrected address
    corrected_address = " ".join(corrected_tokens)
    return corrected_address

# Example input address with intentional spelling mistakes
input_address = """Addres

EGHOSHPARA 4 NO WARD, KALYANI,
Kalyani, Nadia,

West Bengal - 741235"""

# Correct spelling
corrected_address = correct_spelling(input_address)

# Output corrected address
print("Corrected Address:", corrected_address)
