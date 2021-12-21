import requests
import sys

cookie = "53616c7465645f5f3a2bb8e70b7b19d00af66b53520a53cd77587a14553f162ca2eafd24f6b67699492f122d1e664871"

def get_day(n: int):
    r = requests.get(f'https://adventofcode.com/2021/day/{n}/input', cookies={'session': cookie})
    return r.text.strip().split('\n')


def solve(text):
    # Create stack and push and kill chunks
    scores = []
    for line in text:
        score = 0
        stack = []
        for c in line:
            if c in "[{(<":
                # Open chunk
                stack.append(c)
            elif c == ")":
                if stack[-1] != "(":
                    #print(f"String: {line}\tExpected {stack[-1]} found )")
                    break
                else:
                    stack.pop()
            elif c == "}":
                if stack[-1] != "{":
                    #print(f"String: {line}\tExpected {stack[-1]} found curly")
                    break
                else:
                    stack.pop()
            elif c == "]":
                if stack[-1] != "[":
                    #print(f"String: {line}\tExpected {stack[-1]} found ]")
                    break
                else:
                    stack.pop()
            elif c == ">":
                if stack[-1] != "<":
                    #print(f"String: {line}\tExpected {stack[-1]} found >")
                    break
                else:
                    stack.pop()

        else:
            alpha = "({[<"
            score_map = [1, 3, 2, 4]
            mapping = {k:v for (k,v) in zip(alpha, score_map)}
            for c in reversed(stack):
                score *= 5
                score += mapping[c]
            scores.append(score)

    idx = len(scores) // 2
    print(sorted(scores)[idx])


test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n")

solve(test)

#sys.exit()

text = get_day(10)
solve(text)
