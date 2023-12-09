"""--- Day 18: Operation Order ---
As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)). Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:

2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?"""

from operator import add, mul

def evaluate_expression(expr: str) -> int:
    total = 0
    value = ""
    operator = add
    idx = 0
    while idx < len(expr):
        c = expr[idx]
        if c.isdigit():
            value += c
            idx += 1
        elif c == " ":
            idx += 1
        elif c in "*+":
            total = operator(total, int(value))
            value = ""
            operator = add if c == "+" else mul
            idx += 1
        elif c == "(":
            open_brackets = 1
            subexpression = ""

            while open_brackets != 0:
                idx += 1
                if expr[idx] == "(":
                    open_brackets += 1
                elif expr[idx] == ")":
                    open_brackets -= 1
                subexpression += expr[idx]
            idx += 1
            value = str(evaluate_expression(subexpression[:-1]))

    total = operator(total, int(value))

    return total


assert evaluate_expression("1 + 2 * 3 + 4 * 5 + 6") == 71
assert evaluate_expression("1 + (2 * 3) + (4 * (5 + 6))") == 51

assert evaluate_expression("2 * 3 + (4 * 5)") == 26
assert evaluate_expression("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert evaluate_expression("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert evaluate_expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632


with open("data/18.txt") as f:
    expressions = [line.strip() for line in f if line]


print("Part1:", sum(evaluate_expression(expr) for expr in expressions))


# PART 2

"""--- Part Two ---
You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231
Here are the other examples from above:

1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
2 * 3 + (4 * 5) becomes 46.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
What do you get if you add up the results of evaluating the homework problems using these new rules?"""


def evaluate_expression_advanced(expr: str) -> int:
    """
    1 + 2 * 3 + 4 * 5 + 6
    3   * 3 + 4 * 5 + 6
    3   *   7   * 5 + 6
    3   *   7   *  11
        21       *  11
            231
    """
    operator = "+"
    value = ""
    idx = 0
    total = 0

    while idx < len(expr):
        char = expr[idx]
        if char.isdigit():
            value += char
            idx += 1
        elif char == " ":
            idx += 1
        elif char == "+":
            if operator == "+":
                total = total + int(value)
                value = ""
                idx += 1
            operator = char
        elif char == "*":
            total = total + int(value)
            value = ""
            # idx += 1
            # print(total, expr[idx + 1:])
            total = total * evaluate_expression_advanced(expr[idx + 1:])
            idx += len(expr[idx + 1:]) + 1
            # print(total, idx)
            operator = char
        elif char == "(":
            open_brackets = 1
            subexpression = ""

            while open_brackets != 0:
                idx += 1
                if expr[idx] == "(":
                    open_brackets += 1
                elif expr[idx] == ")":
                    open_brackets -= 1
                subexpression += expr[idx]

            idx += 1
            value = str(evaluate_expression_advanced(subexpression[:-1]))
            # print(idx, value)

    if operator == "+":
        total = total + int(value)
    # elif operator == "*":
    #     total = total * int(value)


    return total


assert evaluate_expression_advanced("1 + 2 * 3 + 4 * 5 + 6") == 231
assert evaluate_expression_advanced("1 + (2 * 3) + (4 * (5 + 6))") == 51


assert evaluate_expression_advanced("2 * 3 + (4 * 5)") == 46
assert evaluate_expression_advanced("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert evaluate_expression_advanced("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert evaluate_expression_advanced("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


print("Part2:", sum(evaluate_expression_advanced(expr) for expr in expressions))
