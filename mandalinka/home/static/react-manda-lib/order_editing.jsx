const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));

import RecipeWidget from './recipe_widget.js';
import DeliveryType from './delivery_type.js';
import getCookie from './get_cookie.js';
import Cart from './cart.js';

class OrderEditing extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            date: '...',
            recipes: [],
            thumbnail: '',
            order_id: undefined,
            price: "66.66"
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
                    price: response.price,
                });
            })
            .catch(error => {
                console.log("Chybyčka: ", error);
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

    render() {

        const recipes = [];
        for (let i = 0; i < this.state.recipes.length; i++) {
            recipes.push(
                <RecipeWidget
                    key={i}
                    thumbnail={this.state.recipes[i].thumbnail}
                    title={this.state.recipes[i].title}
                    description={this.state.recipes[i].description}
                    type={this.state.recipes[i].type}
                    attributes={this.state.recipes[i].attributes}
                    alergens={this.state.recipes[i].alergens}
                    order_data={this.state.recipes[i].order_data}
                    price={this.state.recipes[i].price}
                />
            )
        }

        return (
            <div className="order-editing container-fluid position-relative">
                <div className="header d-flex align-items-center mb-3">
                    <div className="me-auto p-2">
                        <h2>Recepty na podelok {this.state.date}</h2>
                    </div>
                    <DeliveryType pickup={this.state.pickup} toggle={this.toggle_pickup}/>
                    <Cart price={this.state.price}/>
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

