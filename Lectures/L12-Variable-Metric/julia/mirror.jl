using LinearAlgebra
using DataFrames
using Random
Random.seed!(1234)

n = 100
α = 0.01

p_ref = rand(n)
p_ref = p_ref/sum(p_ref)
p_ref = (1-α)*p_ref+ones(n)/n*α

#######
## f ##
#######

f = x->sum([(x[i]-p_ref[i])^2/p_ref[i] for i in 1:n])

########
## f' ##
########

fp = x->2*[x[i]/p_ref[i]-1 for i in 1:n]
L = maximum([2/p_ref[i] for i in 1:n])

#######
## π ##
#######

function proj(y)
    u = sort(y, rev=true)
    ρ = findlast(x->x>0, [u[j]+1/j*(1-sum(u[1:j])) for j in 1:n])
    λ = 1/ρ*(1-sum(u[1:ρ]))
    return [max(y[i]+λ, 0) for i in 1:n]
end


#########
## f'' ##
#########

fpp = x->Diagonal([2/p_ref[i] for i in 1:n])

N = 500

####################
## Mirror Descent ##
####################

x = zeros(n, N)
x[:, 1] = rand(n)
x[:, 1] = x[:, 1]/sum(x[:, 1])

gap = zeros(N)
gap[1] = f(x[:, 1])

h = 500/L

for k in 1:N-1
    x[:, k+1] = [x[i, k]*exp(-h*fp(x[:, k])[i]) for i in 1:n]
    x[:, k+1] = x[:, k+1]/sum(x[:, k+1])
    gap[k+1] = f(x[:, k+1])
end

# Results
R = DataFrame(k=1:N, md=gap)
CSV.write("mirror-descent.csv", R)
