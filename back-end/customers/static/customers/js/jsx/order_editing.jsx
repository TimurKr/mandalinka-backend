const root = ReactDOM.createRoot(document.getElementById('current-order'));

import RecipeWidget from './recipe_widget.js';
import DeliveryType from './delivery_type.js';
import getCookie from './get_cookie.js';
import Cart from './cart.js';

class OrderEditing extends React.Component {
    total_price = "66.66"

    constructor(props) {
        super(props);

        this.amount_change = this.amount_change.bind(this);

        this.state = {
            date: '...',
            recipes: undefined,
            thumbnail: '',
            order_id: undefined,
            attributes: undefined,
        }
    }

    componentDidMount() {
        fetch(`/recepty/load_next_order`)
            .then(response => response.json())
            .then(response => {
                this.setState({
                    date: response.date,
                    pickup: response.pickup,
                    recipes: response.recipes,
                    order_id: response.order_id,
                    attributes: response.attributes
                });
                this.set_total_price(response.recipes);
            })
            .catch(error => {
                console.error("Chybyčka: ", error);
            })
    }

    toggle_pickup = () => {
        const put_info = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                order_id: this.state.order_id,
            }),
            mode: 'same-origin',
        };
        
        fetch(`/toggle_pickup`, put_info)
        .then((response) => response.json())
        .then((response) => {
            this.setState({pickup: response.pickup});
        })
    }

    set_total_price = (recipes) => {
        if (this.state.recipes == undefined){
            return;
        }
        if (recipes == undefined) {
            recipes = this.state.recipes;
        }
        var price = 0;
        for (const [key, recipe] of Object.entries(recipes)) {
            price += recipe.price * recipe.amount;
        }
        this.total_price = price;
    }

    amount_change(new_amount, id) {
        this.setState(state => {
            state.recipes[id].amount = new_amount;
            return state;
        })
    }

    render() {

        const recipes = {};
        this.set_total_price();

        if (this.state.recipes != undefined) {

            for (const [rec_key, rec_data] of Object.entries(this.state.recipes)) {
                
                const recipe_attributes = {};
                for(const [attr_key, attr_data] of Object.entries(this.state.attributes)) {
                    if (attr_data.recipes.includes(rec_key)) {
                        recipe_attributes[attr_key] = {
                            favorite: attr_data.favorite,
                            selected: attr_data.selected,
                        }
                    }
                }

                if (recipes[rec_data.type] === undefined) {
                    recipes[rec_data.type] = [];
                }
                recipes[rec_data.type].push(
                    <RecipeWidget
                    key={rec_key}
                    thumbnail={rec_data.thumbnail}
                    title={rec_data.title}
                    description={rec_data.description}
                    type={rec_data.type}
                    attributes={recipe_attributes}
                    alergens={rec_data.alergens}
                    amount={rec_data.amount}
                    recipe_order_instance_id={rec_key}
                    price={rec_data.price}
                    onAmountChange={this.amount_change}
                />)
            }
        }

        const final_recipes = [];
        for (const type of Object.keys(recipes).sort().reverse()) {
            final_recipes.push(
                <div key={type} className="col-md-3 col-12">
                    {recipes[type]}
                </div>
            )
        }

        return (
            <div className="order-editing container-fluid position-relative">
                <div className="header d-flex align-items-center mb-3">
                    <div className="me-auto p-2">
                        <h2>Recepty na podelok {this.state.date}</h2>
                    </div>
                    <div className="d-inline-flex align-items-center">
                        <DeliveryType pickup={this.state.pickup} toggle={this.toggle_pickup}/>
                        <Cart price={this.total_price}/>
                    </div>
                </div>
                <div className="row gx-3 gy-4">
                    {final_recipes}
                </div>
            </div>
        );
    }
}

root.render(
        <OrderEditing />
);

