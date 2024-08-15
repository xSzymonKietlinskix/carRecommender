import React, {useState} from "react";
import HomeIcon from "@mui/icons-material/Home";
import InfoIcon from "@mui/icons-material/Info";
import PhoneRoundedIcon from "@mui/icons-material/PhoneRounded";
import MenuIcon from '@mui/icons-material/Menu';
import { BsCart2 } from "react-icons/bs";
import { HiOutlineBars3 } from "react-icons/hi2";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";

const NavBar = () => {
     const [openMenu, setOpenMenu] = useState(false);
    const menuOptions = [
    {
      text: "Home",
      icon: <HomeIcon />,
    },
    {
      text: "About",
      icon: <InfoIcon />,
    },
    {
      text: "Contact",
      icon: <PhoneRoundedIcon />,
    },
    ];
    return (
        <nav>
            <div className="navbar-menu-container">
            <HiOutlineBars3 onClick={() => setOpenMenu(true)} />
            </div>
            <Drawer open={openMenu} onClose={() => setOpenMenu(false)} anchor="top">
            <Box
              sx={{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}
              role="presentation"
            >
          {menuOptions.map((item) => (
            <ListItem key={item.text} sx={{ width: 'auto' }}>
              <ListItemButton sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <ListItemIcon sx={{ minWidth: 'unset' }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
          <Divider />
        </Box>
      </Drawer>
    </nav>
    )

}
export default NavBar;