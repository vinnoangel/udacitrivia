import React, { Component } from "react";
import $ from "jquery";
import "../stylesheets/FormView.css";

class UserFormView extends Component {
  constructor(props) {
    super();
    this.state = {
      username: "",
      fullname: "",
      gender: "Male",
    };
  }

  submitUser = (event) => {
    event.preventDefault();
    $.ajax({
      url: "http://127.0.0.1:5000/api/v1/users", //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        username: this.state.username,
        fullname: this.state.fullname,
        gender: this.state.gender,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        alert(result.message);
        document.getElementById("add-user-form").reset();
        return;
      },
      error: (error) => {
        alert("Unable to add user. Please try your request again");
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia User</h2>
        <form
          className="form-view"
          id="add-user-form"
          onSubmit={this.submitUser}
        >
          <label>
            Username
            <input
              type="text"
              name="username"
              onChange={this.handleChange}
              required
            />
          </label>
          <label>
            Fullname
            <input
              type="text"
              name="fullname"
              onChange={this.handleChange}
              required
            />
          </label>
          <label>
            Gender
            <select name="gender" onChange={this.handleChange}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default UserFormView;
