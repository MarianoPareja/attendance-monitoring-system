import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="./" className="navbar-title">
        site-title
      </Link>
      <ul>
        <li>
          <Link to="./attendance">Attendance</Link>
        </li>
        <li>
          <Link to="./careers">Careers</Link>
        </li>
        <li>
          <Link to="./schedules">Schedule</Link>
        </li>
        <li>
          <Link to="./students">Students</Link>
        </li>
        <li>
          <Link to="./subjects">Subjects</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
