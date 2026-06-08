using DataFrames
using LinearAlgebra
using CSV

function central_path(μ)

    c = [-2, -1]

    # BARRIER
    M = 2

    F_Q = p->-log(p[1])-log(p[2])-log(1-p[1]-p[2])
    Fp_Q = p->[-1/p[1]+1/(1-p[1]-p[2]), -1/p[2]+1/(1-p[1]-p[2])]
    Fpp_Q = p->[1/p[1]^2+1/(1-p[1]-p[2])^2 1/(1-p[1]-p[2])^2;
                1/(1-p[1]-p[2])^2 1/p[2]^2+1/(1-p[1]-p[2])^2]


    # DN Method
    N = 200
    λ = zeros(N)
    p = zeros(N, 2)
    p[1, :] = [1/3, 1/3]

    for k in 1:N-1
        
        fp = c/μ+Fp_Q(p[k, :])
        fpp = Fpp_Q(p[k, :])
        
        #Newton Decrement
        λ[k] = sqrt(dot(fpp\fp, fp))
        
        # Damped NM
        p[k+1, :] = p[k, :] - (1/(1+λ[k]))*(fpp\fp)
    end

    return p[end, :]
end

μs = exp10.(range(-3, 2, length=200))
P = zeros(length(μs), 3)
for k in 1:length(μs)
    p  = central_path(μs[k])
    P[k, 1] = p[1]
    P[k, 2] = p[2]
    P[k, 3] = 1-p[1]-p[2]
end

R = DataFrame(p1=P[:, 1], p2=P[:, 2], p3=P[:, 3])

CSV.write("cp.csv", R)
