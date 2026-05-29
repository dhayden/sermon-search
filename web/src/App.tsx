import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AppBar, Box, Button, CssBaseline, ThemeProvider, Toolbar, Typography, createTheme } from '@mui/material';
import { MenuBook } from '@mui/icons-material';
import Search from './pages/Search';
import Admin from './pages/Admin';

const theme = createTheme({ palette: { primary: { main: '#6a1b9a' } } });

function Navbar({ tab, setTab }: { tab: string; setTab: (t: string) => void }) {
  return (
    <AppBar position="sticky">
      <Toolbar>
        <Box display="flex" alignItems="center" gap={1} mr={3}>
          <MenuBook />
          <Typography variant="h6" fontWeight="bold">Sermon Scout</Typography>
        </Box>
        <Button color="inherit" component={Link} to="/search" onClick={() => setTab('search')}
          sx={tab === 'search' ? { bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1 } : {}}>
          Search
        </Button>
        <Button color="inherit" component={Link} to="/admin" onClick={() => setTab('admin')}
          sx={tab === 'admin' ? { bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1 } : {}}>
          Manage PDFs
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default function App() {
  const [tab, setTab] = useState('search');
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Navbar tab={tab} setTab={setTab} />
        <Routes>
          <Route path="/" element={<Navigate to="/search" replace />} />
          <Route path="/search" element={<Search />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
