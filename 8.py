import requests
import itertools

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    map1 = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
    map2 = {}
    alpha = "abcdefg"
    for i, x in enumerate("abcdefg"):
        map2[x] = i
    tot = 0
    for line in text:
        data, obs = line.split(' | ')
        data, obs = [x.split() for x in [data, obs]]
        for setting in itertools.permutations(range(7)):
            for word in data + obs:
                # Try to map the word to a number
                letters = sorted([alpha[setting[map2[c]]] for c in list(word)])
                new_word = ''.join(letters)
                if new_word not in map1:
                    break
            else:
                string = ''
                for s in obs:
                    letters = sorted([alpha[setting[map2[c]]] for c in list(s)])
                    new_word = ''.join(letters)
                    string += str(map1.index(new_word))

                tot += int(string)
                break
    print(tot)


test = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split('\n')

solve(test)

text = get_day(8)
solve(text)
