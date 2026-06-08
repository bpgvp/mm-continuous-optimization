using DataFrames

N = 15
xs = 1/7

x = zeros(N)
x[1] = 0.01
gap = zeros(N)

for k in 1:N-1
    x[k+1] = 2*x[k] - 7*x[k]^2
    gap[k+1] = abs(x[k+1]-1/7)
end

R = DataFrame(N=1:N, gap=gap)
