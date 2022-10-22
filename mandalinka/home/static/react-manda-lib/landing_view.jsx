const root_div = document.getElementById('Account');
const root = ReactDOM.createRoot(root_div);


class AccountIcon extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      isHovering: false,
      isAuthenticated: root_div.getAttribute("is_authenticated"),
    };
    this.myAccountLink = root_div.getAttribute("my_account_link");
    this.logOutLink = root_div.getAttribute("log_out_link");
    this.newUserLink = root_div.getAttribute("new_user_link");
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this)
  }


  handleMouseOver(e) {
    this.setState({ isHovering: true });
  }

  handleMouseOut(e) {
    this.setState({ isHovering: false });
  }
  render() {

    if (this.state.isAuthenticated === "True") {
      return (
        <div id="AccountIcons" className="position-absolute top-0 end-0" onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut}>
          {
            this.state.isHovering
          ?
            <div className="btn-group-vertical">
              <a>
                <span id="Person" className="material-symbols-rounded menu">
                  person
                </span>
              </a>
              <a href={this.myAccountLink} >
                <span id="ManageAccount" className="material-symbols-rounded option">
                  manage_accounts
                </span>
                <span className="custom-tooltip">Upravte si profil</span>
              </a>
              <a href={this.logOutLink}>
                <span  id="LogOut" className="material-symbols-rounded option">
                  logout
                </span>
                <span className="custom-tooltip">Odhláste sa</span>
              </a>
            </div>
          :
            <div className="btn-group-vertical">
              <a>
                <span id="Person" className="material-symbols-rounded menu">
                  person
                </span>
              </a>
            </div>
          }
        </div>
      )
    } else {
      return (
        <div id="AccountIcons" className="position-absolute top-0 end-0" onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut}>
          {
            this.state.isHovering
          ?
            <div className="btn-group-vertical">
              <a>
                <span id="Person" className="material-symbols-rounded menu">
                  person
                </span>
              </a>
              <a href="#" data-bs-toggle="modal" data-bs-target="#LoginModal">
                <span id="LoginModalButton" className="material-symbols-rounded option">
                  login
                </span>
                <span className="custom-tooltip">Prihláste sa</span>

              </a>
              <a href={this.newUserLink}>
                <span id="SignUp" className="material-symbols-rounded option">
                  person_add
                </span>
                <span className="custom-tooltip">Vytvorte si účet</span>
              </a>
            </div>
          :
            <div className="btn-group-vertical">
              <a>
                <span id="Person" className="material-symbols-rounded menu">
                  person
                </span>
              </a>
            </div>
          }
        </div>
      )
    }
  }
}

root.render(<AccountIcon />)