const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));

import RecipeWidget from './recipe_widget.js';

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
                    recipes: response.recipes,
                });
            })
            .catch(error => {
                console.log("Chybyčka: ", error);
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

root.render(
        <OrderEditing />
);

