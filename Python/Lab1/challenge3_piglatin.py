import enchant as e

def english_to_pig_latin(input_word):
    vowels = set(["a" , "e" , "i" , "o", "u"])
    consonants = set(["b" , "c" , "d" , "f" , "g" , "h" , "j" , "k" , "l" , "m" , "n" , "p" , "q" , "r" , "s" , "t" , "v" , "w" , "x" , "y" , "z"])
    result = ""
    # firs i create a set of vowels and consonants, and an empty string to
    # store the final result
    for index,elem in enumerate(input_word):
        if index == 0 and elem.lower() in consonants and elem.lower() != "y":
            # check the fist character if it's consonants AND it's not 'y'
            for i in range(len(input_word)):
                # if it is, then keep looping until
                # we find a character in vowels set
                if input_word[i].lower() in vowels:
                    consonant_part = input_word[0 : i]
                    # once we found a vowel, slice the
                    # input word from the beginning until
                    # i (excluding), the index where we found the vowel
                    vowel_start = input_word[i : ]
                    # slice the input word again, by starting
                    # from where we found the vowel, till the end
                    result  = vowel_start + consonant_part + "ay"
                    # to get the result, merge all of them,
                    # i.e: the result form the two slicings
                    # and add "ay" in the end
                    break
        
        if index == 0 and elem.lower() == "y":
            # same concept as before, except that
            # look for why, and at the end instead
            # of adding "ay", we add "ey"
            for i in range(len(input_word)):
                if input_word[i].lower() in vowels:
                    consonant_part = input_word[0 : i]
                    vowel_start = input_word[i : ]
                    result  = vowel_start + consonant_part + "ey"
                    break

        # here i tackle the hyphenated edge case
        if "-" in input_word:
            words = input_word.split("-")
            # basically, split it, take it out first from
            # the input string, then we treat them individually 
            result = ""
            for word in words:
                result = result + english_to_pig_latin(word) + "-"
                # then merge it with the empty result string
                # and apply the pig_latin_to_english to the splitted word
                # then in between them add back the "-"
            result = result[:-1]
            # then put it back in result, by slicing.
        
        if input_word[-1] in [".", "!", "," , ":", ";"]:
            result = english_to_pig_latin(input_word[:-1]) + input_word[-1]
            # check if there's any punctuation in the end of the
            # input_word. If there is, use the english_to_pig_latin
            # from the beginning to the end but excluding the punctuation
            # at the end. Then just add the punctuation back by doing input_word[-1]
                
        if index == 0 and elem.lower() in vowels:
            result = input_word + "yay"
            # if the first one is a vowel, then nothing
            # much to do but add aloha at the end
    return result
 

def pig_latin_to_english(input_word):
    result = ""
    dict_Check = e.Dict('en_US')
    if input_word[-1] in [".", "!", "," , ":", ";"]:
        result = pig_latin_to_english(input_word[:-1]) + input_word[-1]
    # here, i deal with input word containing punctuation.
    # if there is punctuation, then i apply the function
    # to the word, excluding the punctuation, then just put it back
    # in by indexing it with -1.

    if "-" in input_word:
        words = input_word.split("-")
        result = ""
        for word in words:
            result = result + pig_latin_to_english(word) + "-"
        result = result[:-1]
    # if the word is hyphenated, just treat them independently
    # like what i did with english_to_pig_latin() function
    # then just put the hyphen back in

    if input_word[-3:] == "yay":
        result = input_word[:-3]
    # if it's a vowel-starting word, then
    # check if last 3 is yay, then it must be it,
    # i check it using slicing. Then put it 
    # in result, excluding last 3, by slicing again

    elif input_word[-2:] == "ay" or input_word[-2:] == "ey":
        string = input_word[:-2]
        word = string
        while not dict_Check.check(word):
            last_char = word[-1] 
            word = last_char + word[:-1]
        result = word
    # here checking for the ones starting with consonants,
    # they must contain "ay" or "ey" in the end.
    # then I go back to the end of the word, not
    # including "ay" or "ey", and keep picking
    # up the character and put it back to the front.
    # I loop this with a while loop and stops once
    # pyenchant dictionary confirms it's a valid word.

    return result


out1 = english_to_pig_latin("Quotient")
out2 = pig_latin_to_english(out1)
print(out1)
print(out2)

out1 = english_to_pig_latin("Mustn't")
out2 = pig_latin_to_english(out1)
print(out1)
print(out2)

out1 = english_to_pig_latin("Yellow")
out2 = pig_latin_to_english(out1)
print(out1)
print(out2)

out1 = english_to_pig_latin("Awesome!")
out2 = pig_latin_to_english(out1)
print(out1)
print(out2)

out1 = english_to_pig_latin("Car")
out2 = pig_latin_to_english(out1)
print(out1)
print(out2)




















