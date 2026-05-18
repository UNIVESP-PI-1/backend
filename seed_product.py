from models import db, Category, User
from sqlalchemy.orm import sessionmaker
from services import product_service

Session = sessionmaker(bind=db)
session = Session()

class ProductSchema:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.category_id = kwargs.get('category_id')
        self.sku = kwargs.get('sku')
        self.barcode = kwargs.get('barcode')
        self.cost_price = kwargs.get('cost_price', 0)
        self.sale_price = kwargs.get('sale_price', 0)
        self.stock_quantity = kwargs.get('stock_quantity', 0)
        self.min_stock = kwargs.get('min_stock', 0)
        self.status = kwargs.get('status', True)

def run_seed():
    print("🚀 Iniciando a semeadura de Categorias e Produtos...")

    user = session.query(User).first()
    if not user:
        print("❌ Erro: Nenhum usuário encontrado no banco. Execute o seed de usuário primeiro!")
        session.close()
        return
    
    operator_id = user.id
    print(f"👤 Utilizando o usuário '{user.name}' (ID: {operator_id}) como operador padrão.")

    categories_data = {
        "Copa e Alimentação": {
            "description": "Produtos de consumo rápido diário que exigem reposição constante.",
            "products": [
                {"name": "Café em Pó Tradicional 500g", "sku": "ALM-CAF-500", "min_stock": 10, "stock": 25, "barcode": "7891000123456"},
                {"name": "Açúcar Refinado 1kg", "sku": "ALM-ACU-001", "min_stock": 5, "stock": 15, "barcode": "7891000123457"},
                {"name": "Biscoito Cream Cracker 400g", "sku": "ALM-BIS-CC4", "min_stock": 8, "stock": 20, "barcode": "7891000123458"},
                {"name": "Biscoito Recheado Chocolate 130g", "sku": "ALM-BIS-CHO", "min_stock": 12, "stock": 30, "barcode": "7891000123459"}
            ]
        },
        "Descartáveis": {
            "description": "Itens volumosos com alto giro de estoque.",
            "products": [
                {"name": "Copo Descartável 200ml (Caixa c/ 2500 un)", "sku": "DSC-COP-200", "min_stock": 2, "stock": 5, "barcode": "7891000123460"},
                {"name": "Copo Descartável para Café 50ml (Pacote c/ 100 un)", "sku": "DSC-COP-050", "min_stock": 5, "stock": 12, "barcode": "7891000123461"},
                {"name": "Guardanapo de Papel (Pacote c/ 50 folhas)", "sku": "DSC-GUA-050", "min_stock": 10, "stock": 40, "barcode": "7891000123462"},
                {"name": "Mexedor de Café Plástico (Pacote c/ 500 un)", "sku": "DSC-MEX-500", "min_stock": 3, "stock": 8, "barcode": "7891000123463"}
            ]
        },
        "Higiene e Limpeza": {
            "description": "Produtos essenciais para a manutenção do ambiente de trabalho.",
            "products": [
                {"name": "Detergente Líquido Neutro 500ml", "sku": "LIM-DET-NEU", "min_stock": 6, "stock": 18, "barcode": "7891000123464"},
                {"name": "Papel Toalha Interfolha (Pacote c/ 1000 folhas)", "sku": "LIM-PAP-TOA", "min_stock": 4, "stock": 10, "barcode": "7891000123465"},
                {"name": "Sabonete Líquido Refil 1L", "sku": "LIM-SAB-LIQ", "min_stock": 3, "stock": 7, "barcode": "7891000123466"}
            ]
        },
        "Material de Escritório": {
            "description": "Complementa as demandas de escritório do almoxarifado corporativo.",
            "products": [
                {"name": "Papel A4 Sulfite Branco (Resma c/ 500 folhas)", "sku": "ESC-PAP-A4", "min_stock": 5, "stock": 15, "barcode": "7891000123467"},
                {"name": "Caneta Esferográfica Azul (Caixa c/ 50 un)", "sku": "ESC-CAN-AZU", "min_stock": 2, "stock": 6, "barcode": "7891000123468"}
            ]
        }
    }

    for cat_name, cat_info in categories_data.items():
        category = session.query(Category).filter(Category.name == cat_name).first()
        
        if not category:
            category = Category(name=cat_name, description=cat_info["description"])
            session.add(category)
            session.flush()
            print(f"📁 Categoria criada: '{cat_name}'")
        else:
            print(f"📁 Categoria existente identificada: '{cat_name}'")

        for prod in cat_info["products"]:
            existing_product = session.query(product_service.Product).filter(product_service.Product.sku == prod["sku"]).first()
            
            if not existing_product:
                schema = ProductSchema(
                    name=prod["name"],
                    description=f"Item de cadastro inicial para {cat_name}.",
                    category_id=category.id,
                    sku=prod["sku"],
                    barcode=prod["barcode"],
                    cost_price=1000,
                    sale_price=1500,
                    stock_quantity=prod["stock"],
                    min_stock=prod["min_stock"],
                    status=True
                )
                
                product_service.create(schema=schema, session=session, user_id=operator_id)
                print(f"  📦 Produto adicionado: {prod['name']} (Estoque: {prod['stock']})")
            else:
                print(f"  ⚠️ Produto já existente pulado: {prod['name']} (SKU: {prod['sku']})")

    print("\n✅ Seed executado com sucesso! Banco atualizado e logs de movimentações integrados.")
    session.close()

if __name__ == "__main__":
    run_seed()
    