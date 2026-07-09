from flask import Flask, render_template, request
from scipy.optimize import linprog
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'chave_secreta_enade'
app = app

@app.route('/')
def index():
    # Carrega a página inicialmente sem resultados
    return render_template('index.html', dados=None, resultado=None)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # 1. Coleta dos dados digitados ou padrões do formulário
        m_mesa = float(request.form.get('manaus_mesa', 8000))
        m_cadernos = float(request.form.get('manaus_cadernos', 1000))
        m_netbooks = float(request.form.get('manaus_netbooks', 2000))
        m_custo = float(request.form.get('manaus_custo', 150000))

        s_mesa = float(request.form.get('sul_mesa', 2000))
        s_cadernos = float(request.form.get('sul_cadernos', 1000))
        s_netbooks = float(request.form.get('sul_netbooks', 7000))
        s_custo = float(request.form.get('sul_custo', 210000))

        d_mesa = float(request.form.get('demanda_mesa', 16000))
        d_cadernos = float(request.form.get('demanda_cadernos', 6000))
        d_netbooks = float(request.form.get('demanda_netbooks', 28000))

        # Dicionário para devolver os dados inseridos de volta para os inputs
        dados = {
            'manaus_mesa': m_mesa, 'manaus_cadernos': m_cadernos, 'manaus_netbooks': m_netbooks, 'manaus_custo': m_custo,
            'sul_mesa': s_mesa, 'sul_cadernos': s_cadernos, 'sul_netbooks': s_netbooks, 'sul_custo': s_custo,
            'demanda_mesa': d_mesa, 'demanda_cadernos': d_cadernos, 'demanda_netbooks': d_netbooks
        }

        # Configuração do solver (Minimização)
        c = [m_custo, s_custo]
        # Multiplica por -1 pois linprog usa restrições do tipo <= por padrão
        A = [
            [-m_mesa, -s_mesa],
            [-m_cadernos, -s_cadernos],
            [-m_netbooks, -s_netbooks]
        ]
        b = [-d_mesa, -d_cadernos, -d_netbooks]
        bounds = [(0, None), (0, None)]

        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if res.success:
            x = round(res.x[0], 2)
            y = round(res.x[1], 2)
            custo_total = round(res.fun, 2)

            # Cálculos das conferências passo a passo para a tela
            parcial_manaus = round(m_custo * x, 2)
            parcial_sul = round(s_custo * y, 2)
            
            check_mesa = round((m_mesa * x) + (s_mesa * y), 2)
            check_cadernos = round((m_cadernos * x) + (s_cadernos * y), 2)
            check_netbooks = round((m_netbooks * x) + (s_netbooks * y), 2)

            resultado = {
                'x': x, 'y': y, 'custo_total': f"{custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                'parcial_manaus': f"{parcial_manaus:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                'parcial_sul': f"{parcial_sul:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                'check_mesa': check_mesa, 'check_cadernos': check_cadernos, 'check_netbooks': check_netbooks
            }
            return render_template('index.html', dados=dados, resultado=resultado)
        else:
            return render_template('index.html', dados=dados, error="Não foi possível encontrar uma solução viável.")

    except Exception as e:
        return render_template('index.html', dados=dados, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from scipy.optimize import linprog
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'chave_secreta_enade'

@app.route('/')
def index():
    return render_template('index.html', dados=None, resultado=None)

# ... suas outras rotas aqui ...

# Adicione isso no final
def handler(request):
    return app(request)
