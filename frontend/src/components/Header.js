import React from "react";
import { Navbar, Container, Nav ,NavDropdown} from "react-bootstrap";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../actions/auth";
const Header = () => {
  const userInfo = useSelector((state) => state.userLogin);
  const { user, error, loading } = userInfo;
  const dispatch = useDispatch();
  return (
    <div>
      <Navbar bg="primary" expand="lg" variant="dark">
        <Container>
          <Navbar.Brand as={Link} to="/">
            AlmatyComplaint
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse
            id="basic-navbar-nav"
            className="justify-content-end"
          >
            <Nav className="ml-auto">
              {user ? (
                <>
                  <Nav.Link as={Link} to="/profile" className="disabledCursor">
                    Профиль
                  </Nav.Link>
                  <Nav.Link
                    as={Link}
                    to="/"
                    className="disabledCursor"
                    onClick={(e) => dispatch(logout())}
                  >
                    Шығу
                  </Nav.Link>
                </>
              ) : (
                <Nav.Link as={Link} to="/login">
                  Кіру
                </Nav.Link>
              )}
              {user && user.is_admin && 
                        <NavDropdown title={`${user.first_name} (Admin)`} id="basic-nav-dropdown">
                        <NavDropdown.Item as={Link} to='/admin/category'>Категория</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to='/admin/users'>Қолданушылар</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to='/admin/complaints'>Шағымдар</NavDropdown.Item>
                      </NavDropdown>
              }
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
};

export default Header;
