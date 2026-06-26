using LinearAlgebra
using DataFrames
using CSV
using Random
Random.seed!(1234)

n = 2500

#######
## f ##
#######

f = x->-sum([log(x[i]) for i in 1:n])

########
## f' ##
########

fp = x->[-1/x[i] for i in 1:n]

#########
## f'' ##
#########

fpp = x->Diagonal([1/x[i]^2 for i in 1:n])

fstar = f([1/n for _ in 1:n])
N = 30

function backtrack(f, fp, x, d, c)

    # Backtrack parameter
    ρ = 0.8
    
    # Full feasible step
    α = minimum([minimum([-x[i]/d[i] for i in findall(s->s<0, d)])*0.99, 1])
    
    while f(x+α*d) > f(x) + c*α*dot(fp(x), d) && α>=1e-7
        α *= ρ
    end
    
    return α
end

###################
## Newton Method ##
###################

x = zeros(n, N)
x[:, 1] = rand(n)
x[:, 1] = x[:, 1]/sum(x[:, 1])

gap = zeros(N)
step = zeros(N)
gap[1] = f(x[:, 1])-fstar

for k in 1:N-1
    KKT_M = [fpp(x[:, k]) ones(n); ones(n)' 0]
    KKT_B = [fpp(x[:, k])*x[:, k]; 0]

    # Search direction
    d_k = (KKT_M\KKT_B)[1:end-1]

    # Step-size rule using backtracking
    step[k] = backtrack(f, fp, x[:, k], d_k, 0.5)

    x[:, k+1] = x[:, k] + step[k]*d_k
    gap[k+1] = abs(f(x[:, k+1])-fstar)
end

# Results
R = DataFrame(k=1:N, full=gap, step=step)
CSV.write("newton-method.csv", R)
