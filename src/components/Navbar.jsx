import React, { useState } from "react";
import { Avatar, Dropdown, Button, Drawer, Badge, Space } from "antd";
import { Link, useNavigate } from "react-router-dom";
// import logoImage from "../assets/mainLogo.svg";
import {
  MenuOutlined,
  BellOutlined,
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
} from "@ant-design/icons";

const Navbar = ({ showDrawer }) => {
  const navigate = useNavigate();

  const [drawerVisible, setDrawerVisible] = useState(false);

  const handleOnClicktoHome = () => {
    navigate("/");
  };

  const handleSignOut = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const profileMenuItems = [
    {
      key: "profile",
      label: (
        <Link to="/profile" className="flex items-center gap-2 px-1 py-2">
          <UserOutlined /> Profile
        </Link>
      ),
    },
    {
      key: "logout",
      label: (
        <span
          onClick={handleSignOut}
          className="flex items-center gap-2 px-1 py-2 hover:bg-gray-100"
        >
          <LogoutOutlined /> Logout
        </span>
      ),
    },
  ];

  return (
    <header className="w-full bg-[#FFFFFF] shadow-sm fixed top-0 z-50 py-[6px] ">
      <div className=" mx-2 lg:ml-[30px] lg:mr-24 ">
        <div className="flex items-center justify-between h-16 ">
          {/* Left section */}
          <div className="flex items-center">
            <Button
              type="text"
              className="md:hidden mr-2"
              icon={<MenuOutlined className="text-lg" />}
              onClick={showDrawer}
            />

            <button
              onClick={handleOnClicktoHome}
              className="flex items-center space-x-1 lg:space-x-2 xl:space-x-3 logo-container cursor-pointer lg:mr-4"
            >
              {/* Header Logo */}
              <div className="mt-3">
                <h2 className="text-3xl font-bold text-gray-500">
                  Trade Pilot
                </h2>
              </div>
            </button>

          </div>

          {/* Right section */}
          <div className="flex items-center gap-4 lg:gap-8">
            {/* <Badge
              count={10}
              size="small"
              className="cursor-pointer p-2 rounded-full bg-gray-300 hover:text-blue-500 transition-colors"
            >
              <BellOutlined
                className="text-2xl"
                onClick={() => setDrawerVisible(true)}
              />
            </Badge> */}

            <Dropdown
              menu={{ items: profileMenuItems }}
              trigger={["click"]}
              placement="bottomRight"
              overlayClassName="w-48"
            >
              <Avatar
                icon={<UserOutlined className="" />}
                size="large"
                className="cursor-pointer border border-gray-300 hover:opacity-80 transition-opacity"
              />
            </Dropdown>
          </div>
        </div>
      </div>

      <Drawer
        title="Notifications"
        placement="right"
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
        width={300}
        styles={{
          body: { padding: 0 }
        }}
      >
        <div className="p-4">
          <p>No new notifications</p>
        </div>
      </Drawer>
    </header>
  );
};

export default Navbar;
