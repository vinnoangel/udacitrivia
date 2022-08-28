import React, { Component } from "react";
import "../stylesheets/App.css";
import User from "./User";
import Search from "./Search";
import "../stylesheets/User.css";
import $ from "jquery";

class UserView extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      page: 1,
      totalUsers: 0,
    };
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers = () => {
    $.ajax({
      url: `http://127.0.0.1:5000/api/v1/users?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          users: result.users,
          totalUsers: result.total_users,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load users. Please try your request again");
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getUsers());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalUsers / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? "active" : ""}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `http://127.0.0.1:5000/api/v1/users/search`, //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          users: result.users,
          totalUsers: result.total_users,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load users. Please try your request again");
        return;
      },
    });
  };

  userAction = (id) => (action) => {
    if (action === "DELETE") {
      if (window.confirm("are you sure you want to delete the user?")) {
        $.ajax({
          url: `http://127.0.0.1:5000/api/v1/users/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            alert(result.message);
            this.getUsers();
          },
          error: (error) => {
            alert("Unable to load users. Please try your request again");
            return;
          },
        });
      }
    }

    // Track user games
    else if (action === "TRACK-GAME") {
    }
  };

  render() {
    return (
      <div className="user-view">
        <div className="users-list">
          <h2>Quick Menu</h2>
          <ul>
            <li>
              <a href="/add-user">Add User</a>
            </li>
            <li>
              <a href="/users">Users</a>
            </li>
            <li>
              <a href="/user-games">Track User Games</a>
            </li>
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className="table-list">
          <table id="users">
            <caption>
              <h2>Users</h2>
            </caption>
            <thead>
              <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Gender</th>
                <th>Created At</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {this.state.users.map((q, ind) => (
                <User
                  key={q.id}
                  username={q.username}
                  fullname={q.fullname}
                  gender={q.gender}
                  created_at={q.created_at}
                  id={q.id}
                  userAction={this.userAction(q.id)}
                />
              ))}
            </tbody>
          </table>
          <br></br>
          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default UserView;
