import clingo

def on_model(model):
    print model

def on_finish(res):
    print res

prg = clingo.Control()
prg.load("defTest.lp")
prg.ground([("definitions", [])])
solveFuture = prg.solve_async(on_model, on_finish)
solveFuture.wait()
