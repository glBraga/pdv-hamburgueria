import os
import flet as ft

def main(page: ft.Page):
    # Configurações da Janela
    page.title = "PDV Hamburgueria"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # 1. ESTADO
    pedido_atual = {}

    # 2. ELEMENTOS VISUAIS (Atualizado para ft.Colors)
    lista_ui = ft.ListView(expand=True, spacing=10)
    total_ui = ft.Text("Total: R$ 0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)

    # 3. LÓGICA DE ATUALIZAÇÃO DA TELA
    def atualizar_tela():
        lista_ui.controls.clear()
        valor_total = 0
        
        for nome, dados in pedido_atual.items():
            qtd = dados['qty']
            preco = dados['price']
            subtotal = qtd * preco
            valor_total += subtotal
            
            # Linha do item com o botão de diminuir
            # (Atualizado para ft.Icons e ft.Colors)
            lista_ui.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{qtd}x {nome}", weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(f"R$ {preco:.2f} cada"),
                    trailing=ft.Row([
                        ft.Text(f"R$ {subtotal:.2f}", weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                            icon_color=ft.Colors.RED_400,
                            on_click=lambda e, n=nome: remover_item(n)
                        )
                    ], alignment=ft.MainAxisAlignment.END, tight=True)
                )
            )
        
        total_ui.value = f"Total: R$ {valor_total:.2f}"
        page.update()

    # 4. LÓGICA DE AÇÕES (Cliques)
    def adicionar_item(nome, preco):
        if nome in pedido_atual:
            pedido_atual[nome]['qty'] += 1
        else:
            pedido_atual[nome] = {'price': preco, 'qty': 1}
        atualizar_tela()

    def remover_item(nome):
        if nome in pedido_atual:
            if pedido_atual[nome]['qty'] > 1:
                pedido_atual[nome]['qty'] -= 1
            else:
                del pedido_atual[nome]
        atualizar_tela()

    def limpar_pedido(e):
        pedido_atual.clear()
        atualizar_tela()

    # 5. BASE DE DADOS DE PRODUTOS (Atualizado para ft.Icons)
    produtos = [
        {"nome": "X-Burguer", "preco": 32.00, "icone": ft.Icons.LUNCH_DINING},
        {"nome": "X-Salada", "preco": 36.00, "icone": ft.Icons.LUNCH_DINING},
        {"nome": "Losito", "preco": 48.00, "icone": ft.Icons.LUNCH_DINING},
        {"nome": "Coca-Cola", "preco": 6.50, "icone": ft.Icons.LOCAL_DRINK},
        {"nome": "Agua", "preco": 5.00, "icone": ft.Icons.LOCAL_DRINK},
        {"nome": "Fritas", "preco": 30.00, "icone": ft.Icons.FASTFOOD},
    ]

    # 6. MONTAGEM DA INTERFACE DE BOTÕES
    botoes_produtos = ft.GridView(
        runs_count=2,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )
    
    for p in produtos:
        botoes_produtos.controls.append(
            ft.ElevatedButton(
                content=ft.Column([
                    ft.Icon(p['icone'], size=40), 
                    ft.Text(p['nome'], text_align=ft.TextAlign.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=lambda e, n=p['nome'], pr=p['preco']: adicionar_item(n, pr),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            )
        )

    # 7. ADICIONANDO TUDO NA TELA (Atualizado para ft.Colors)
    page.add(
        ft.Text("Cardápio", size=20, weight=ft.FontWeight.BOLD),
        botoes_produtos,
        ft.Divider(height=20, color=ft.Colors.BLACK_12),
        ft.Text("Resumo do Pedido", size=20, weight=ft.FontWeight.BOLD),
        lista_ui,
        ft.Divider(height=20, color=ft.Colors.BLACK_12),
        total_ui,
        ft.ElevatedButton("Finalizar / Novo Pedido", on_click=limpar_pedido, bgcolor=ft.Colors.RED_500, color=ft.Colors.WHITE, width=page.window_width)
    )

# Novo padrão para iniciar a aplicação no Flet 0.80+ sem gerar avisos
porta = int(os.environ.get("PORT", 8000))
ft.app(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=porta)