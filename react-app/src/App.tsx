import Navbar from "./components/Navbar";

import Attendance from "./components/pages/Attendance";
import Carreer from "./components/pages/Careers";
import Schedule from "./components/pages/Schedule";
import Student from "./components/pages/Students";
import Subject from "./components/pages/Subjects";

import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <>
      <div className="main-container">
        <Navbar></Navbar>
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Attendance />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/careers" element={<Carreer />} />
            <Route path="/schedules" element={<Schedule />} />
            <Route path="/students" element={<Student />} />
            <Route path="/subjects" element={<Subject />} />
          </Routes>
        </div>
      </div>
    </>
  );
}

export default App;
