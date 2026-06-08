using Contour
using CSV
using DataFrames

"""
    relative_entropy(P, Q)

    Relative entropy between two distributions P and Q.
"""
function relative_entropy(P, Q)
    d = length(P)
    I = NaN

    if(minimum(P)>=0 && minimum(Q)>0 && sum(P)==1 && sum(Q)==1)
        I = 0
        for i = 1:d
            if (P[i]>0 && Q[i]>0)
                I = I + P[i]*log(P[i]/Q[i])
            elseif (P[i]>0 && Q[i]==0) 
                I = NaN
            end
        end
    end

    return I
end

# Grid the probability simplex
Δ = 0.001
P_ref = [1.5/8, 2/8, 4.5/8]

# Compute function
F = [relative_entropy([p1, p2, 1-p1-p2], P_ref) for p1 in 0:Δ:1, p2 in 0:Δ:1] 

# Compute contour lines
c = contours(0:Δ:1, 0:Δ:1, F, [0.001, 0.01, 0.04, 0.1, 0.2, 0.4, 0.8, 1.6])

# Save contour lines
name=[]
for cl in Contour.levels(c)
    open("contour_"*string(level(cl))*".tex", "w") do f
    
        for j in 1:length(Contour.lines(cl))
            line = Contour.lines(cl)[j]
            p1, p2 = coordinates(line)
            C=DataFrame(p1=p1, p2=p2, p3=1-p1-p2)
            C=C[find(s->!isnan(s), C[:p3]), :]
            if size(C, 1)>1
              println("C: ", C) CSV.write("csv/contour_"*string(level(cl))*"_"*string(j)*".csv", C; quotechar=''')
                write(f, "\\addplot3  [draw=black, densely dotted] table [x=p1,y=p2, z=p3, col sep=comma] {csv/contour_"string(level(cl))*"_"*string(j)*".csv}; \n")
            end
            
        end
        
    
    end
end


