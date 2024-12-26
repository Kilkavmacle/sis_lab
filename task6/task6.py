import json

class FLP:
    def ld_js(self, fp):
        with open(fp, 'r') as f:
            return json.load(f)

    def mem(self, val, f_set):
        """Вычисляет степени принадлежности для четкого значения."""
        mems = {}
        for t, pts in f_set.items():
            mems[t] = max(
                self.intrp(val, pts[i], pts[i + 1])
                for i in range(len(pts) - 1)
                if pts[i][0] <= val <= pts[i + 1][0]
            ) if any(pts[i][0] <= val <= pts[i + 1][0] for i in range(len(pts) - 1)) else 0
        return mems

    def intrp(self, x, p1, p2):
        """Линейная интерполяция между двумя точками."""
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:  # Вертикальная линия
            return max(y1, y2)
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def rules(self, f_in, tr):
        """Применяет правила переходов к фаззифицированным данным."""
        f_out = {}
        for t, d in f_in.items():
            if t in tr:
                ot = tr[t]
                f_out[ot] = max(f_out.get(ot, 0), d)
        return f_out

    def crisp(self, f_res, o_set):
        """Вычисляет четкое значение из фаззифицированного результата."""
        num = sum(
            d * self.cent(o_set[t])
            for t, d in f_res.items() if d > 0
        )
        den = sum(d for d in f_res.values() if d > 0)
        return num / den if den > 0 else 0

    def cent(self, pts):
        """Находит центр масс для множества точек."""
        return sum(x for x, _ in pts) / len(pts)

    def proc(self, in_f, reg_f, tr_f, el):
        in_d = self.ld_js(in_f)
        reg_d = self.ld_js(reg_f)
        tr_d = self.ld_js(tr_f)

        f_in = self.mem(el, in_d)
        print("Фаззифицированное значение:", f_in)

        f_out = self.rules(f_in, tr_d)
        print("Результат с правил переходов:", f_out)

        c_out = self.crisp(f_out, reg_d)
        print("Дефаззифицированное значение:", c_out)

        return c_out

if __name__ == "__main__":
    p = FLP()
    in_f = './input.json'
    reg_f = './regulator.json'
    tr_f = './transition.json'
    el = 19.3

    p.proc(in_f, reg_f, tr_f, el)
