import { Menu } from "antd";
import {
  AppstoreOutlined,
  ContainerOutlined,
  SettingOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { FaUsers } from "react-icons/fa";
import { MdOutlinePayment, MdLeaderboard } from "react-icons/md";
import { FaBuildingFlag } from "react-icons/fa6";
import { SlBadge } from "react-icons/sl";
import { TbPackages } from "react-icons/tb";

// import { signOutAdmin } from "../api/api";

const { SubMenu } = Menu;

const Sidebar = ({ onClick }) => {
  const location = useLocation();

  const navigate = useNavigate();
  const handleSignOut = () => {
    // signOutAdmin();
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  // Determine the selected key based on current route
  const getSelectedKey = () => {
    const path = location.pathname;
    // if (path === "/") return ["dashboard"];
    if (path === "/users") return ["users"];
    if (path === "/profile") return ["settings", "setting-profile"];
    if (path === "/privacy-policy") return ["settings", "privacy-policy"];
    return ["dashboard"];
  };

  const sidebarItems = [
    // {
    //   key: "dashboard",
    //   icon: <AppstoreOutlined />,
    //   label: <Link to="/">Dashboard</Link>,
    // },
    {
      key: "users",
      icon: <FaUsers />,
      label: <Link to="/users">User Management</Link>,
    },

    // Logout item pinned to bottom — use a clickable label so the handler runs reliably
    {
      key: "logout",
      icon: <LogoutOutlined />,
      label: (
        <span
          onClick={handleSignOut}
          className="flex items-center px-3 py-2 w-full hover:bg-gray-100"
        >
          Logout
        </span>
      ),
      className: "bottom-20",
      style: {
        position: "absolute",
        width: "100%",
      },
      danger: true,
    },
  ];

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
      }}
    >
      <Menu
        mode="inline"
        selectedKeys={getSelectedKey()}
        items={sidebarItems}
        onClick={onClick}
        style={{
          height: "calc(100% - 64px)",
          backgroundColor: "#ffffff",
          color: "#002436",
        }}
      />
    </div>
  );
};

export default Sidebar;

