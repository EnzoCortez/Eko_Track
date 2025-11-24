import os

# Create directory if not exists
os.makedirs('templates/admin', exist_ok=True)

content = """{% extends 'admin/master.html' %}

{% block body %}
<div class="container-fluid">
    <div class="row">
        <div class="col-md-12">
            <h1>Panel de Control Eko Track</h1>
            <hr>
        </div>
    </div>

    <div class="row">
        <!-- Criticality Matrix -->
        <div class="col-md-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Matriz de Criticidad (Reportes Pendientes)</h3>
                </div>
                <div class="panel-body">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>Categoría</th>
                                <th>Alta</th>
                                <th>Media</th>
                                <th>Baja</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in matrix_data %}
                            <tr>
                                <td>{{ row.category }}</td>
                                <td class="danger">{{ row.high }}</td>
                                <td class="warning">{{ row.medium }}</td>
                                <td class="success">{{ row.low }}</td>
                                <td><strong>{{ row.total }}</strong></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Suggested Interventions (Budget) -->
        <div class="col-md-6">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Sugerencias de Intervención (Presupuesto: ${{ budget }})</h3>
                </div>
                <div class="panel-body">
                    <p>Priorización basada en: <strong>Prioridad de Categoría * Volumen de Reportes</strong></p>
                    <table class="table table-condensed">
                        <thead>
                            <tr>
                                <th>Categoría (Score)</th>
                                <th>Costo Estimado</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in budget_suggestions %}
                            <tr class="{% if item.funded %}success{% else %}danger{% endif %}">
                                <td>{{ item.category }} ({{ item.score }})</td>
                                <td>${{ item.cost }}</td>
                                <td>{% if item.funded %}Financiado{% else %}Sin Fondos{% endif %}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <p><strong>Total Asignado: ${{ spent }}</strong></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
