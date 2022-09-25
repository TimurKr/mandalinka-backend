const root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));


class RecipeWidget extends React.Component {
    constructor(props) {
        super(props);
        this.state = {pornum: 9}
    }
    render() {
        return (
            <div className="col-md-3 col-sm-6">
                <div className="card">
                    <img src="..." className="card-img-top" alt="..."/>
                    <div className="card-body">
                        <h5 className="card-title">Card title</h5>
                        <p className="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                        <a href="#" className="btn btn-primary">Go somewhere</a>
                    </div>
                </div>
            </div>
        )
    }
}

class OrderEditing extends React.Component {

    render() {
        return (
            <div className="container-fluid">
                <div className="row g-2">
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                    <RecipeWidget />
                </div>
            </div>
        );
    }
}


root.render(<OrderEditing />);

