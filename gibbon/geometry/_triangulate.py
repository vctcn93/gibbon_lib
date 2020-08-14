import numpy as np


class Triangulator:
    def __init__(self, points):
        points = self.flip_points(points)
        points = np.flip(points, axis=0)
        self.points = points

    def flip_points(self, points):
        return np.array([[pt[0], pt[1], 0] for pt in points])

    def triangulate(self):
        indices = list()

        if len(self.points) < 3:
            return indices

        vertices = [None] * len(self.points)

        if self.area > 0:
            for v in range(len(self.points)):
                vertices[v] = v

        else:
            for v in range(len(self.points)):
                vertices[v] = (len(self.points) - 1) - v

        nv = len(self.points)
        count = 2 * nv
        m = 0
        v = nv - 1

        while nv > 2:
            count -= 1

            if count <= 0:
                return indices

            u = v
            if nv <= u:
                u = 0

            v = u + 1
            if nv <= v:
                v = 0

            w = v + 1
            if nv <= w:
                w = 0

            if self.snip(u, v, w, nv, vertices):
                # int a, b, c, s, t;
                a = vertices[u]
                b = vertices[v]
                c = vertices[w]
                indices.append(a)
                indices.append(b)
                indices.append(c)
                m += 1
                s = v
                t = v + 1

                while t<nv :
                    vertices[s] = vertices[t]
                    s += 1
                    t += 1
                nv -= 1
                count = 2 * nv

        indices.reverse()
        return np.array(indices).reshape(-1, 3).tolist()

    @property
    def area(self):
        n = len(self.points)
        area = 0
        p = n - 1
        q = 0

        while q < n:
            pval = self.points[p]
            qval = self.points[q]
            area += pval[0] * qval[1] - qval[0] * pval[1]
            p = q
            q += 1

        return area * .5

    def snip(self, u, v, w, n, vertices):
        epsilon = .00000000001
        a = self.points[vertices[u]]
        b = self.points[vertices[v]]
        c = self.points[vertices[w]]

        if epsilon > (((b[0] - a[0]) * (c[1] - a[1])) - ((b[1] - a[1]) * (c[0] - a[0]))):
            return False

        for p in range(n):
            if (p == u) or (p == v) or (p == w):
                continue

            pt = self.points[vertices[p]]

            if self.inside_triangle(a, b, c, pt):
                return False

        return True

    def inside_triangle(self, a, b, c, p):
        ax = c[0] - b[0]
        ay = c[1] - b[1]
        bx = a[0] - c[0]
        by = a[1] - c[1]
        cx = b[0] - a[0]
        cy = b[1] - a[1]
        apx = p[0] - a[0]
        apy = p[1] - a[1]
        bpx = p[0] - b[0]
        bpy = p[1] - b[1]
        cpx = p[0] - c[0]
        cpy = p[1] - c[1]

        a_cross_bp = ax * bpy - ay * bpx
        c_cross_ap = cx * apy - cy * apx
        b_cross_cp = bx * cpy - by * cpx

        return (a_cross_bp >= 0.0) and (b_cross_cp >= 0.0) and (c_cross_ap >= 0.0)


if __name__ == '__main__':
    points = [
        [851765.3138225847, -1100795.49156665],
        [854150.3339251439, -1101850.9896086205],
        [857726.2499381255, -1085011.5786730011],
        [894692.5585027611, -1085054.180631406],
        [909002.5677365252, -1088228.6897246342],
        [900657.9473761542, -1120853.5943264698],
        [889925.5239427302, -1118735.863439467],
        [864883.4252557936, -1113443.3896610164],
        [861306.0621173917, -1113439.248583559],
        [852958.6587865269, -1111324.1114300534],
        [849381.2956101584, -1111319.959202751]
    ]

    tr = Triangulator(points)
    indices = tr.triangulate()
    print(tr.area)
    print(indices)
