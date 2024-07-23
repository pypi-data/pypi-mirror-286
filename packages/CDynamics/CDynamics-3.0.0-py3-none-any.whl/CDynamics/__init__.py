import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

class Julia:
    def __init__(self,expr,lite=False):
        z = sp.symbols('z')
        self.expr = expr
        self.eval = sp.lambdify(z,expr) 
        if not lite:
            self.critical_points = [complex(float(sp.re(i)),float(sp.im(i))) for i in sp.solve(expr.diff(),z)]
            try:
                self.fixed_points = [complex(float(sp.re(i)),float(sp.im(i))) for i in sp.solve(expr-z,z)]
            except Exception:
                self.fixed_points = [complex(i.n()) for i in sp.solve(expr-z,z)]
            if self.expr.limit(z,sp.oo)==sp.oo or self.expr.limit(z,sp.oo)==-sp.oo:
                self.fixed_points.insert(0,np.inf)
    def grid(a=-1,b=1,c=-1,d=1,resx=300,resy=300):
        xvals, yvals = np.meshgrid(np.linspace(a,b,resx), np.linspace(c,d,resy)[::-1])
        return xvals+1j*yvals
    def orbit(self,seed,depth,bail_out):
        o = [seed]
        for i in range(depth):
            z = self.eval(o[-1])
            if abs(z)<bail_out:
                o.append(z)
            else:
                break
        return(o)
    def plot(self,a=-1,b=1,c=-1,d=1,resx=500,resy=500,depth=25,bail_out=1000,filled=True,glow=0,
             cmap='binary',scale=1,critical_orbit_depth=0,fixed_points=False,
             cols=[(61, 64, 91),(244, 241, 222), (224, 122, 95),(129, 178, 154),(242, 204, 143)],alpha=1):
        grid = Julia.grid(a,b,c,d,resx,resy)
        def orb(z):
            o = [z]
            for i in range(depth):
                z = self.eval(o[-1])
                if abs(z)<bail_out:
                    o.append(z)
                else:
                    break
            return(o)
        def cfp_winf(z):
            def cfp(z):
                can = self.fixed_points[(np.abs(np.array(self.fixed_points)-z)).argmin()]
                if np.abs(can-z)<1:
                    return(can)
                else:
                    return(np.inf)
            t=len(orb(z))
            return(
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][0]+(t*glow*0.299)),
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][1]+(t*glow*0.587)),
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][2]+(t*glow*0.114))
                )    
        def cfp_wo_inf(z):
            def cfp(z):
                return(self.fixed_points[(np.abs(np.array(self.fixed_points)-z)).argmin()])
            t=len(orb(z))
            return(
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][0]+(t*glow*0.299)),
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][1]+(t*glow*0.587)),
                int(cols[self.fixed_points.index(cfp(orb(z)[-1]))][2]+(t*glow*0.114))
                )
        def plot_orbit(orb):
            orb_mod = [[(orb[i].real+b)*(resx/(b-a)),(orb[i].imag+d)*(resy/(d-c))] for i in range(len(orb))]
            for i in range(len(orb_mod)-1):
                ax.add_artist(ConnectionPatch(orb_mod[i],orb_mod[i+1],"data","data",arrowstyle="->"))
        fig, ax = plt.subplots()
        if filled:
            if self.expr.limit(z,sp.oo)==sp.oo or self.expr.limit(z,sp.oo)==-sp.oo:
                plot = np.vectorize(cfp_winf)(grid)
            else:
                plot = np.vectorize(cfp_wo_inf)(grid)
            plot = np.stack([plot[0], plot[1], plot[2]], axis=-1,dtype=float)
            plot = (plot - np.min(plot))/(np.max(plot)-np.min(plot))
            im = ax.imshow(plot,aspect=(d-c)/(b-a),alpha=alpha) 
        else:
            orb_len = lambda o: len(orb(o))
            plot = np.vectorize(orb_len)(grid)
            im = ax.imshow(plot,cmap=cmap,aspect=(d-c)/(b-a),alpha=alpha)
        ydim,xdim = plot.shape[:2]
        ax.set_yticks([0,ydim/2,ydim])
        ax.set_yticklabels([c, (d+c)/2, d])
        ax.set_xticks([0,xdim/2,xdim])
        supress = ax.set_xticklabels([a, (a+b)/2, b])
        fig.set_figheight(scale*5)
        fig.set_figwidth(scale*5)
        if critical_orbit_depth<=0:
            pass
        elif critical_orbit_depth==1:
            ax.scatter([(z.real+b)*(resx/(b-a)) for z in self.critical_points],[(z.imag+d)*(resy/(d-c)) for z in self.critical_points],c='Black',s=2)
        else:
            orbs = [self.orbit(self.critical_points[i],critical_orbit_depth,1000) for i in range(len(self.critical_points))]
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in self.critical_points],[(z.imag+d)*(resy/(d-c)) for z in self.critical_points],c='Black')
            [plot_orbit(orbs[i]) for i in range(len(orbs))]
        if fixed_points == True:
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in self.fixed_points],[(z.imag+d)*(resy/(d-c)) for z in self.fixed_points],c='Black',marker='x')