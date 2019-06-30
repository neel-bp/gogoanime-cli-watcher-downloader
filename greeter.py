def greeter():
  ansi="""
  ___        ___   ___
 / _ \      (_) \ / / |
/ /_\ \_ __  _ \ V /| |
|  _  | '_ \| |/   \| |
| | | | | | | / /^\ \_|
\_| |_/_| |_|_\/   \(_)
"""
  print('\u001b[32;1m'+ansi+'\u001b[0m')
  for x in range(0,24):
    print('\u001b[33;1m'+chr(22)+'\u001b[0m',end='')
  print()
  print()