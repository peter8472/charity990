def print_results(results):
  for row in results:
     rval=[str(i) for i in row.values()]
     print(" ".join(rval))

