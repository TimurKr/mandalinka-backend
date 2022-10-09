export default class Cart extends React.Component {
	render() {
		return (
			<div>
				<a type="button" className="cart btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
					{this.props.price + ' €'}
				</a>

				<div className="modal fade" id="exampleModal" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
					<div className="modal-dialog">
						<div className="modal-content">
							<div className="modal-header">
								<h1 className="modal-title fs-5" id="exampleModalLabel">
									Objendávka
								</h1>
								<button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
							</div>
							<div className="modal-body">
								Tu bude raz zoznam objednávky
							</div>
						</div>
					</div>
				</div>
			</div>
		)
	}
}