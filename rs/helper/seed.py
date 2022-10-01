def get_seed_string(seed: float) -> str:
    seed_string = ""
    chars = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    leftover = seed  # here long to unsigned string?
    if leftover < 0:
        leftover += 18446744073709551616
    charCount = len(chars)
    while leftover >= 1:
        remainder = int(leftover % charCount)
        leftover -= remainder
        leftover = leftover // charCount  # need // because that allows for some integer division to keep big floats accurate
        char = chars[remainder]
        seed_string += char
    return seed_string[::-1]


def make_seed_string_number(seed: str) -> float:
    total = 0
    seed_str = seed.upper().replace("O", "0")
    chars = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    for c in seed_str:
        if c not in chars:
            raise Exception("Bad Seed!")
        r = chars.index(c)
        total *= len(chars)
        total += r
    return total


"""
  public static long getLong(String seedStr) {
    long total = 0L;
    seedStr = seedStr.toUpperCase().replaceAll("O", "0");
    for (int i = 0; i < seedStr.length(); i++) {
      char toFind = seedStr.charAt(i);
      int remainder = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ".indexOf(toFind);
      if (remainder == -1)
        System.out.println("Character in seed is invalid: " + toFind); 
      total *= "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ".length();
      total += remainder;
    } 
    return total;
  }
  
  
  public static String getString(long seed) {
    StringBuilder bldr = new StringBuilder();
    BigInteger leftover = new BigInteger(Long.toUnsignedString(seed));
    BigInteger charCount = BigInteger.valueOf("0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ".length());
    while (!leftover.equals(BigInteger.ZERO)) {
      BigInteger remainder = leftover.remainder(charCount);
      leftover = leftover.divide(charCount);
      int charIndex = remainder.intValue();
      char c = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ".charAt(charIndex);
      bldr.insert(0, c);
    } 
    return bldr.toString();
  }
"""
