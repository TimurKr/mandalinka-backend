const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));

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
        console.log(`In amount change, id:${id}, new_amount: ${new_amount}, total_price: ${this.total_price}`);
        console.log(`Attempt to change: `, this.state.recipes[id].amount)
        // this.setState({
        //     recipes: {
        //         ... this.state.recipes,
        //         id: {
        //             ... this.state.recipes[id],
        //             amount: new_amount,
        //         }
        //     }
        // })
        this.setState(state => {
            state.recipes[id].amount = new_amount;
            return state;
        })
        
        console.log(`In amount change, id:${id}, new_amount: ${new_amount}, total_price: ${this.total_price}`);
    }


    render() {

        const recipes = [];
        this.set_total_price();

        if (this.state.recipes != undefined) {

            for (const [key, value] of Object.entries(this.state.recipes)) {
                recipes.push(
                    <RecipeWidget
                    key={key}
                    thumbnail={value.thumbnail}
                    title={value.title}
                    description={value.description}
                    type={value.type}
                    attributes={value.attributes}
                    alergens={value.alergens}
                    amount={value.amount}
                    recipe_order_instance_id={key}
                    price={value.price}
                    onAmountChange={this.amount_change}
                />)
            }
        }

        return (
            <div className="order-editing container-fluid position-relative">
                <div className="header d-flex align-items-center mb-3">
                    <div className="me-auto p-2">
                        <h2>Recepty na podelok {this.state.date}</h2>
                    </div>
                    <DeliveryType pickup={this.state.pickup} toggle={this.toggle_pickup}/>
                    <Cart price={this.total_price}/>
                </div>
                <div className="row gx-3 gy-4">
                    {recipes}
                </div>
            </div>
        );
    }
}

root.render(
        <OrderEditing />
);

