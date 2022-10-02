const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));

class Alergens extends React.Component {
    constructor(props) {
        super(props);
        this.state = {allergens: props.data}
    }

    get_print_codes(list) {
        let print_codes = []
        list.forEach(allergen => {
            print_codes.push(allergen[0])
        })
        if (print_codes.length == 0) {
            return 'Žiadne alergény'
        }
        return 'Alergény: ' + print_codes.join(', ')
    }

    render(){
        return (
            <div>
                <p className="text-end m-0 p-1">{this.get_print_codes(this.state.allergens)}</p>
            </div>
        )
    }
}

class OrderdInterface extends React.Component {
    
    constructor(props) {
        super(props);
        this.minus_sign_enabled = 
            <a role="button" onClick={this.remove_portions}>
                <i className="bi bi-dash-circle-fill enabled"/>
            </a>
        this.minus_sign_disabled = 
            <i className="bi bi-dash-circle-dotted disabled"/>
        this.plus_sign_enabled = 
            <a role="button" onClick={this.add_portions}>
                <i className="bi bi-plus-circle-fill enabled"/>
            </a>
        this.plus_sign_disnabled = 
            <i className="bi bi-plus-circle-dotted disabled"/>

        let minus_sign;
        let plus_sign;
        let active;
        if (props.data.value === 0) {
            minus_sign = this.minus_sign_disabled;
            plus_sign = this.plus_sign_enabled;
            active = 'inactive'
        } else if (props.data.value > 0) {
            minus_sign = this.minus_sign_enabled;
            plus_sign = this.plus_sign_enabled;
            active = 'active';
        } else {
            console.error("Invalid value in OrderInterface");
        };

        this.state = {
            value: props.data.value,
            class: 'btn btn-primary',
            minus_sign: minus_sign,
            plus_sign: plus_sign,
            active: active,
            recipe_id: props.data.recipe_order_instance_id,
        };

        this.remove_portions = this.remove_portions.bind(this);
        // this.statics.recipe_id = props.data.recipe_order_instance_id;
    }

    add_portions = () => {
        
        const put_info = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'X-CSRFToken': Cookies.get('csrftoken'),
            },
            body: JSON.stringify({
                recipe: this.state.recipe_id,
                new_value: this.state.value + 2,
            }),
            mode: 'same-origin',
        };
        fetch(`/edit_order`, put_info)
        .then((answer) => {
            if (answer == 'OK') {
                this.setState({value: this.state.value + 2})
            } else {
                console.error(answer)
            }
        })
        console.log('add_portions');
    }

    remove_portions(){
        console.log('remove_portions', this);
    }

    render() {
        
        return (
            <div className={'hstack gap-2 px-2 bg-primary rounded-pill order-interface allign-middle position-absolute top-0 end-0 translate-middle-y ' + this.state.active}>
                {this.state.minus_sign}
                <h3 className="m-0"> {this.state.value} </h3>
                {this.state.plus_sign}
            </div>

            // <div className="btn-group position-absolute top-0 end-0 translate-middle-y">
            //     <button type="button" className={this.state.class}>-</button>
            //     <button type="button" className={this.state.class}>{this.state.value}</button>
            //     <button type="button" className={this.state.class}>+</button>
            // </div>
        )
    }
}

class RecipeWidget extends React.Component {
    constructor(props) {
        super(props);
        const attributes = [];
        props.data.attributes.forEach(attr => {
            attributes.push(
                <div className="m-1 px-2 bg-primary text-light rounded-5 font-size-sm" key={attr}>
                    {attr}
                </div>
            )
        })       

        this.state = {
            title: props.data.title,
            description: props.data.description,
            thumbnail: props.data.thumbnail,
            type_color: props.data.type_color,
            attributes: attributes,
            alergens: props.data.alergens,
            order_data: props.data.order_data,
        }
    }

    render() {
        
        return (
            <div className="col-md-3 col-sm-6 col-6">
                <div className="card position-relative" style={{background: this.state.type_color}}>
                    <div className="card-body p-2 pb-0">
                        <div className="bg-light rounded-2">
                            <img src={this.state.thumbnail} className="card-img-top rounded-2" alt='img_alt'></img>
                            <h4 className="card-title px-2 mt-2">{this.state.title}</h4>
                            <p className="card-text px-2 m-0">{this.state.description}</p>
                            <div className="d-flex flex-wrap justify-content-center">
                                {this.state.attributes}
                            </div>
                        </div>
                        <Alergens data={this.state.alergens}/>
                    </div>
                    <OrderdInterface data={this.state.order_data}/>
                </div>
            </div>
        )
    }
}

class OrderEditing extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            date: '...',
            recipes: [],
            thumbnail: '',
        }

        
    }

    componentDidMount() {
        fetch(`/recepty/load_next_order`)
        .then(response => response.json())
        .then(response => {
            this.setState({
                date: response.date,
                recipes: response.recipes
            });
        })
        .catch(error => {
            console.log("Error: ", error);
        })
    }

    render() {

        const recipes = [];
        for (let i = 0; i < this.state.recipes.length; i++) {
            recipes.push(
                <RecipeWidget 
                    key={i} 
                    data={this.state.recipes[i]}
                    />
            )
        }

        return (
            <div className="container-fluid">
            <h2 className="mb-4">Recepty na najbližšiu objednávku z dňa {this.state.date}</h2>
                <div className="row gx-2 gy-4">
                    {recipes}
                </div>
            </div>
        );
    }
}


root.render(<OrderEditing />);

