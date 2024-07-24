#write a python program on count the vowels and consonants in given string

def count_vowels_consonants(string):
    vowels_letter = "aeiouAEIOU"
    vowel_count = 0
    cons_count = 0
    for char in string:
        if char.isalpha():
            if char in vowels_letter:
                #print(char)
                vowel_count = vowel_count+1
            else:
                cons_count = cons_count+1
    print("Vowel count",vowel_count,"Consonant count",cons_count)
