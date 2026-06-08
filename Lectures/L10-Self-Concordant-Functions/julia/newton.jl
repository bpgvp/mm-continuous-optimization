using DataFrames

xs = 1/7
x0 = 1

x = zeros(N)
x[1] = x0
λ = zeros(N)

fp = x->7-1/x
fpp = x->1/x^2

gap = zeros(N)
gap[1] = x0-xs
N = 15
for k in 1:N-1
    λ[k] = sqrt(fpp(x[k])^(-1)*fp(x[k])^2)
    if λ[k]>(3-sqrt(5))/2
        x[k+1] = x[k] - fpp(x[k])^(-1)*fp(x[k])/(1+λ[k])
    else
        x[k+1] = x[k] - fpp(x[k])^(-1)*fp(x[k])
    end
    gap[k+1] = abs(x[k+1]-xs)
end

R = DataFrame(N=1:N, gap=gap)
