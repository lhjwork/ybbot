const calcRem = (size) => `${size / 16}rem`;

const SettingSmallContent = {
    FONTMAILY: 'Roboto',
    FONTSIZES: '12px',
    FONTWEIGHT: 'normal',
    LINEHEIGHT: '14px',
};
const fontFamliySetting = {
    BASE: 'Roboto',
    BOLD: 'bold',
    STYLE: 'normal',
};
const fontSizes = {
    NAVSIZE: calcRem(20),
    BASE: calcRem(16),
};
const colorTheme = {
    MAIN: '#ADCCEF',
    GRAY: '#555555',
    LIGHTGRAY: '#E3E5E5',
    SKYBLUE: '#7ABDFF',
    WHITE: '#fff',
    BLACK: '#000',
    LIGHTBLUE: '#9BBCE0',
    Blue: '#1a3d98',
};
const componentSize = {
    SIDEBARWIDTH: calcRem(260),
    NAVHEIGHT: '60px',
    MENUHEIGHT: '50px',
};
export const deviceSizes = {
    mobileS: '320px',
    mobileM: '375px',
    mobileL: '450px',
    tablet: '1024px',
    tabletL: '1024px',
    mobileXL: '768px',
};
// export const light = {
//     colors: {
//         bgColor: '#fff',
//         font_color: '#000',
//         name: 'blue',
//         viewCount: 'purple',
//         projectStack: '#000',
//         link: '#000',
//     },
// };
// export const dark = {
//     colors: {
//         MAINCOLOR: '#3D4863',
//         GRAY: '#555555',
//         PLACEHOLDER: '#C4C4C4',
//         // bgColor: '#2d333b',
//         // font_color: '#adbac7',
//         // name: 'black',
//         // viewCount: '#aa9e9e',
//         // projectStack: '#403b3b',
//         // link: '#04f898',
//     },
// };
export const isDevice = {
    mobileS: window.matchMedia('(max-width: 320px)').matches,
    mobileM: window.matchMedia('(max-width: 375px)').matches,
    mobileL: window.matchMedia('(max-width: 450px)').matches,
    tablet: window.matchMedia('(max-width: 1024px)').matches,
    tabletL: window.matchMedia('(max-width: 1024px)').matches,
    mobileXL: window.matchMedia('(max-width: 768px)').matches,
};
const device = {
    mobileS: `only screen and (max-width: ${deviceSizes.mobileS})`,
    mobileM: `only screen and (max-width: ${deviceSizes.mobileM})`,
    mobileL: `only screen and (max-width: ${deviceSizes.mobileL})`,
    tablet: `only screen and (max-width: ${deviceSizes.tablet})`,
    tabletL: `only screen and (max-width: ${deviceSizes.tabletL})`,
    mobileXL: `only screen and (max-width: ${deviceSizes.mobileXL})`,
};
const theme = {
    SettingSmallContent,
    fontSizes,
    colorTheme,
    componentSize,
    fontFamliySetting,
    device,
};

export default theme;
