import React, { Component } from "react";
import "../stylesheets/User.css";

class User extends Component {
  render() {
    const { username, fullname, gender, created_at, id } = this.props;
    console.log(id);
    return (
      <tr>
        <td>{fullname}</td>
        <td>{username}</td>
        <td>{gender}</td>
        <td>{created_at}</td>
        <td>
          <img
            src="delete.png"
            alt="delete"
            className="delete"
            title="Delete User"
            onClick={() => this.props.userAction("DELETE")}
          />{" "}
          <img
            className="delete"
            alt="games"
            src="art.svg"
            title="Track Games"
            onClick={() => this.props.userAction("TRACK-GAME")}
          />
        </td>
      </tr>
    );
  }
}

export default User;
