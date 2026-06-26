using LinearAlgebra
using DataFrames
using CSV
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
μ = minimum([2/p_ref[i] for i in 1:n])

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

################################
## Projected Gradient Descent ##
################################
h = 2/(L+μ)

x = zeros(n, N)
x[:, 1] = rand(n)
x[:, 1] = x[:, 1]/sum(x[:, 1])

gm = zeros(N)
gm[1] = f(x[:, 1])

for k in 1:N-1
    x[:, k+1] = proj(x[:, k] - h*fp(x[:, k]))
    gm[k+1] = f(x[:, k+1])
end

GM = DataFrame(gm=gm)

############################
## Efficiency Estimate GM ##
############################

ub = [L/2*((L-μ)/(L+μ))^(2k)*norm(x[:, 1]-p_ref)^2 for k in 1:N]

E = DataFrame(gm_e=ub,)

##################################
## Accelerated Gradient Descent ##
##################################
h = 1/L
x = zeros(n, N)
x[:, 1] = rand(n)
x[:, 1] = x[:, 1]/sum(x[:, 1])
y = zeros(n, N)
y[:, 1] = x[:, 1]
nm = zeros(N)
nm[1] = f(x[:, 1])

for k in 1:N-1
    x[:, k+1] = proj(y[:, k] - h*fp(y[:, k]))
    y[:, k+1] = x[:, k+1]+(sqrt(L)-sqrt(μ))/(sqrt(L)+sqrt(μ))*(x[:, k+1]-x[:, k])
    nm[k+1] = f(x[:, k+1])
end

NM = DataFrame(nm=nm)

############################
## Efficiency Estimate NM ##
############################

nm_ee = [minimum([4*L/(2*sqrt(L)+k*sqrt(μ))^2, L*(1-sqrt(μ/L))^k])*((f(x[:, 1])-0)+μ/2*(norm(x[:, 1]-p_ref)^2)) for k in 1:N]

E2 = DataFrame(nm_e=nm_ee)

# Results
R = hcat(DataFrame(k=1:N), GM, E, NM, E2)
CSV.write("gradient-methods.csv", R)
