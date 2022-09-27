const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));


class RecipeWidget extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: props.data.title,
            description: props.data.description,
            thumbnail: props.data.thumbnail
        }
    }

    render() {
        return (
            <div className="col-md-3 col-sm-6">
                <div className="card">
                    <div className="card-body">
                        <img src={this.state.thumbnail} className="card-img-top" alt='img_alt'></img>
                        <h5 className="card-title">{this.state.title}</h5>
                        <p className="card-text">{this.state.description}</p>
                        <a href="#" className="btn btn-primary">Go somewhere</a>
                    </div>
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
            recipes.push(<RecipeWidget 
                key={i} 
                data={this.state.recipes[i]}
                />)
        }

        return (
            <div className="container-fluid">
            <h2>Recepty na najbližšiu objednávku z dňa {this.state.date}</h2>
                <div className="row g-2">
                    {recipes}
                </div>
            </div>
        );
    }
}


root.render(<OrderEditing />);

