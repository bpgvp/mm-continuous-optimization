using DataFrames
using LinearAlgebra

c = [-2, -1]

# BARRIER
ν = 3
M = 2

F_Q = p->-log(p[1])-log(p[2])-log(1-p[1]-p[2])
Fp_Q = p->[-1/p[1]+1/(1-p[1]-p[2]), -1/p[2]+1/(1-p[1]-p[2])]
Fpp_Q = p->[1/p[1]^2+1/(1-p[1]-p[2])^2 1/(1-p[1]-p[2])^2;
            1/(1-p[1]-p[2])^2 1/p[2]^2+1/(1-p[1]-p[2])^2]


# IP Method
β = 1/10
δ = 1.4/(1+10*sqrt(ν))
N = 200
μ = zeros(N)
μ[1] = 1
λ = zeros(N)
p = zeros(N, 2)

p[1, :] = [0.05, 0.5]

R = DataFrame(p1=Real[], p2=Real[], p3=Real[], T=AbstractString[])

for k in 1:N-1
    
    fp = c/μ[k]+Fp_Q(p[k, :])
    fpp = Fpp_Q(p[k, :])

    #Newton Decrement
    λ[k] = sqrt(dot(fpp\fp, fp))

    if λ[k]>β
        # Not Centered
        # Damped NM
        push!(R, [p[k, 1], p[k, 2], 1-p[k, 1]-p[k ,2], "NC"])
        μ[k+1] = μ[k] 
        p[k+1, :] = p[k, :] - 1/(1+λ[k])*fpp\fp
    else
        push!(R, [p[k, 1], p[k, 2], 1-p[k, 1]-p[k ,2], "C"])
        μ[k+1] = μ[k]/(1+δ)
        fp = c/μ[k+1]+Fp_Q(p[k, :])
        fpp = Fpp_Q(p[k, :])
        p[k+1, :] = p[k, :] - fpp\fp
    end
    
    println("λ=", λ[k])
    println("μ_-=", μ[k+1])
    println("p=", p[k, :])
    
end

R_nc = R[findall(s->s=="NC", R[:T]), :]
R_c  = R[findall(s->s=="C", R[:T]), :]

# CSV.write("ip_nc.csv", R_nc)
# CSV.write("ip_c.csv", R_c)
# CSV.write("ip.csv", R)

