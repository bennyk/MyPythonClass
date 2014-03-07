import re

def f1(line):
    m = re.match(r"^(\w+)\((.*)\)", line)
    if m is not None:
        return line if len(m.group(2)) == 0 else f1(m.group(2))
    else:
        raise SyntaxError('parse error at %s' % line)

def f2(line, start=0):
    assert isinstance(line, str)
    # print(line[start:])
    x = line[start:]
    startpos = line.find('(', start)
    if startpos >= 0:
        # f1() => indicates position of ')'
        endpos = line.find(')', f2(line, start=startpos+1) + 1)
        assert endpos >= 0, "expecting closing parenthesis at %s^" % line[start:]

        if endpos >= 0:
            print(line[start:startpos], '<-', line[startpos:endpos+1])

        return endpos

    else:
        # backtrack
        return start - 1

def f3(line, start=0):

    x = line[start:]
    ri = re.finditer(r'[()]', line[start:])
    try:
        m = next(ri)
        startpos = start + m.start()
        c = line[startpos]
        if c == '(':
            # nextpos indicates pos of ')'
            nextpos = f3(line, startpos + 1)
            m2 = re.search(r'(\w+)', line[start:startpos])
            print(line[start:startpos], '<-', line[startpos:nextpos+1])
            # print(m2.group(1), '<-', line[startpos:nextpos+1])
            return f3(line, nextpos+1)
        elif c == ')':
            return startpos

    except StopIteration:
        pass



# print(f('foo(boo(moo(la, li, lu), foo()))'))
print(f3('foo(moo(xoo, coo()), boo())'))


