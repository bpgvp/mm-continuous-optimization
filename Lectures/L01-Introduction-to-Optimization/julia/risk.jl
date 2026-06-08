# Tested with JULIA v1.3.1

using JuMP
using Clp
using DataFrames

n = 100000
r = range(-10, stop=100, length=n)

m = Model(Clp.Optimizer)

# probability
@variable(m, p[1:n] >= 0)
@constraint(m, sum(p) == 1)

# Prior informatoin
@constraint(m, 15 <= sum((r).*p) <= 20)
@constraint(m, 500 <= sum((r.^2).*p) <= 600)
@constraint(m, sum((3*r.^3-2*r).*p) == 40000)

# Objective:
@objective(m, Max, sum(p[findall(x->x<0, r)]))

# Solve
optimize!(m)

println("Probability: ", objective_value(m))
R = DataFrame(Return = r, Prob=value.(p))
