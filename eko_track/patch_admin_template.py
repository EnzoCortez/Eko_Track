import re

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Table Header
if "<th>Asignado</th>" not in content:
    content = content.replace("<th>Costo Estimado</th>", "<th>Costo Estimado</th>\n                                <th>Asignado</th>")
    content = content.replace("<th>Estado</th>", "<th>Estado</th>\n                                <th>Acción</th>")

# Update Table Body
target_row = """                            <tr class="{% if item.funded %}success{% else %}danger{% endif %}">
                                <td>{{ item.category }} ({{ item.score }})</td>
                                <td>${{ item.cost }}</td>
                                <td>{% if item.funded %}Financiado{% else %}Sin Fondos{% endif %}</td>
                            </tr>"""

replacement_row = """                            <tr class="{% if item.funded %}success{% else %}danger{% endif %}">
                                <td>{{ item.category }} ({{ item.score }})</td>
                                <td>${{ item.cost }}</td>
                                <td>${{ item.allocated }}</td>
                                <td>{% if item.funded %}Financiado{% else %}Sin Fondos{% endif %}</td>
                                <td>
                                    <form method="POST" action="/admin/" class="form-inline">
                                        <input type="hidden" name="report_id" value="{{ item.id }}">
                                        <div class="form-group">
                                            <input type="number" name="allocated_amount" class="form-control input-sm" style="width: 80px;" value="{{ item.allocated if item.allocated > 0 else item.cost }}" step="0.01" min="0">
                                        </div>
                                        <button type="submit" class="btn btn-primary btn-xs">Asignar</button>
                                    </form>
                                </td>
                            </tr>"""

content = content.replace(target_row, replacement_row)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
