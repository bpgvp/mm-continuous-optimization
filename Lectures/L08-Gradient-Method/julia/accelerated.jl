# Gradient descent versus Nesterov's accelerated gradient descent on an
# ill-conditioned quadratic f(x) = (L x₁² + μ x₂²)/2.
using LinearAlgebra
using DataFrames
using CSV

L = 1.0
μ = 1e-3                                       # condition number L/μ = 1000

λ = [L, μ]

#######
## f ##
#######

f = x->sum(λ.*x.^2)/2                          # f(x⋆) = 0 at x⋆ = 0

########
## f' ##
########

fp = x->λ.*x

N = 500
x0 = [1.0, 1.0]
D = norm(x0)

######################
## Gradient Descent ##
######################
h = 2/(μ+L)

x = x0
gm = zeros(N+1)
gm[1] = f(x)

for k in 1:N
    global x = x - h*fp(x)
    gm[k+1] = f(x)
end

gm_e = [L*D^2/2*((L-μ)/(L+μ))^(2k) for k in 0:N]

##################################
## Accelerated Gradient Descent ##
##################################
β = (sqrt(L)-sqrt(μ))/(sqrt(L)+sqrt(μ))

x = x0
y = x0
agm = zeros(N+1)
agm[1] = f(x)

for k in 1:N
    x_new = y - fp(y)/L
    global y = x_new + β*(x_new - x)
    global x = x_new
    agm[k+1] = f(x)
end

agm_e = [L*D^2*(1-sqrt(μ/L))^k for k in 0:N]

# Results
R = DataFrame(k=0:N, gm=gm, gm_e=gm_e, agm=agm, agm_e=agm_e)
CSV.write("accelerated.csv", R)
