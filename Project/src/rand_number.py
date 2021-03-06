import math


def LCG(seed, multi, incr, mask):
    """generate a random integer by LCG

    Args:
        seed: seed
        multi: multiplier
        incr: increment
        mask: modulus

    Returns:
        the next integer generated by LCG
    """
    return (seed * multi + incr) & mask


def rand48(seed):
    """generate a random number by RAND48

    Args:
        seed: seed to use for LCG

    Returns:
        a pseudo random integer generated by rand48
    """
    multi = 25214903917
    incr = 11
    mask = 2 ** 48 - 1
    return LCG(seed, multi, incr, mask)


SeedJava = 156079716630527


def post_processing(value):
    """pass the value on 48 bits to 32 bits by deleting the 16 least significant bits

    * shift right 16 bits of value
    * then, if value < 0 then value += 2^32; else return value

    Args:
        value: the integer on 48 bits to pass to 32 bits
    Returns:
        an integer of 32 bits
    """
    value = value >> 16
    if value & 2 ** 31:
        value -= 2 ** 32
    return value


def generator_Java():
    """simulation of pseudo random generator in Java

    Returns:
        a random integer with 2^32 bits
    """
    global SeedJava
    res = rand48(SeedJava)
    # modifying the global seed
    SeedJava = res
    res = post_processing(res)
    return res


def reverse_java_rand48(v1, v2):
    """Giving v1 and v2 on 32 bits generated by generator_Java(), find V1 on 48 bits which

    * V1's 32 most significant bits is equal to v1
    * if use V1 as generator_Java()'s SeedJava, we can get v2 by generator_Java()

    Args:
        v1: 32 bits integer generated by generated_Java()
        v2: 32 bits integer generated by generated_Java()

    Returns:
        the value which satisfied the 2 conditions above

    """
    res = v1 << 16
    while not post_processing(rand48(res)) == v2:
        res += 1
    return res


Index = 0
Seed = 987654321
G = rand48(Seed)


def next_bit():
    """generate pseudo randomly a 0 or 1

    Returns:
        0 or 1
    """
    global Index, G
    b = (G >> Index) % 2
    Index += 1
    if Index == 48:
        Index = 0
        G = rand48(G)
    return b


def rand_int(n):
    """generate a pseudo random number between 0 and n exclusive

    Args:
        n: the exclusive greater border of range
    Returns: (random number, number of rejects)
        * the pseudo number generated
        * the number of rejections
    """
    nb_bits = math.ceil(math.log(n + 1, 2))
    r = n + 1
    rejects = -1
    while r >= n:
        r = 0
        rejects += 1
        for _ in range(nb_bits):
            r = r * 2 + next_bit()
    return r, (rejects + 1) * nb_bits
