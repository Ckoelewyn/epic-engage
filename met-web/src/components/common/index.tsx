import React from 'react';
import { Button as MuiButton, Paper as MuiPaper, Grid, CircularProgress } from '@mui/material';
import styled from '@emotion/styled';

export const RoundedButton = styled(MuiButton)(() => ({
    borderRadius: '23px',
}));

export const StyledPaper = styled(MuiPaper)(() => ({
    border: `1px solid #606060`,
    borderRadius: '4px',
}));

export const MetPaper = ({ children, ...rest }: { children: JSX.Element[] | JSX.Element; [prop: string]: any }) => {
    console.log(rest);
    return (
        <StyledPaper elevation={0} {...rest}>
            {children}
        </StyledPaper>
    );
};

export const Row = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
`;

export const Column = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

export const MidScreenLoader = () => (
    <Grid container direction="row" justifyContent="center" alignItems="center" sx={{ minHeight: '90vh' }}>
        <Grid item>
            <CircularProgress />
        </Grid>
    </Grid>
);
