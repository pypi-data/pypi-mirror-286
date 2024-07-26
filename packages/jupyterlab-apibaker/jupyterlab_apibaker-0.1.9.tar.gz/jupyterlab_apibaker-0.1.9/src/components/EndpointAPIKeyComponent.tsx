import React from 'react'
import { IAPIKey, IEndpoint, IAPIKeyResponse, IAPIKeyListResponse } from '../common/types';
import { CssBaseline, Grid, Typography, TextField, InputAdornment, Tooltip, IconButton, styled, Snackbar, } from '@mui/material';
import APIKeyInfoComponent from './APIKeyInfoComponent';
import NewAPIKeyComponent from './NewAPIKeyComponent';
import { requestAPI } from '../common/requestAPI';
import { CommonContext } from '../contexts/CommonContext';
import { useCurrentEndopintContext } from '../contexts/EndpointContext';
import { Notification } from '@jupyterlab/apputils';
import { IoCopyOutline } from 'react-icons/io5';
import copyToSystem from '../common/copyToClipboard';

const EndpointAPIKeyComponent: React.FC<IEndpoint> = (props): JSX.Element => {
     const { currentUser } = React.useContext(CommonContext) as CommonContextType
     const [apiKeyName, setAPIKeyName] = React.useState<string>('')
     const [apiKeyNameError, setAPIKeyNameError] = React.useState<boolean>(false)
     const [apiKeyDescription, setAPIKeyDescription] = React.useState<string>('')

     const [apiKeys, setAPIKeys] = React.useState<IAPIKey[]>()
     const [adminApiKey, setAdminApiKey] = React.useState<string>()
     const { endpoint } = useCurrentEndopintContext()
     const [snackbarOpen, setSnackbarOpen] = React.useState<boolean>(false)

     const IconButtonWithTooltip = styled(IconButton)({
          root: {
               '&.Mui-disabled': {
                    pointerEvents: 'auto',
               },
          },
     })

     const AlignedInputAdornment = styled(InputAdornment)({
          margin: '0 auto', // fix for vertically unaligned icon
     });

     React.useEffect(() => {
          getAPIKeys()
     }, [])

     const getAPIKeys = async (): Promise<void> => {
          const response = await requestAPI<IAPIKeyListResponse>('api-keys?id=' + encodeURIComponent(props.id) + "&owner=" + encodeURIComponent(currentUser));
          // console.log(`API Keys => ${JSON.stringify(JSON.parse(response.toString()).data, null, 2)}`)          
          console.log(`API Keys => ${JSON.stringify(JSON.parse(response.toString()).data, null, 2)}`)
          setAPIKeys(JSON.parse(response.toString()).data.usersKeys)
          setAdminApiKey(JSON.parse(response.toString()).data.adminKey)
          console.log(adminApiKey);
     }

     const _handleSubmit = async (event: any): Promise<void> => {
          event.preventDefault();
          console.log(`Information to be sent => ${apiKeyName} - ${apiKeyDescription}`)
          const newAPIKey = await requestAPI<IAPIKeyResponse>('api-keys', {
               method: 'POST',
               body: JSON.stringify({
                    current_user: currentUser,
                    endpoint_id: props.id,
                    name: apiKeyName,
                    description: apiKeyDescription
               })
          })
          console.log(`New APIKey => ${JSON.stringify(newAPIKey, null, 2)}`)
          if (newAPIKey.statusCode >= 400) {
               Notification.error(`There has been an error while creating the new API Key: ${apiKeyName}`)
          } else {
               Notification.success(`The new API key ${apiKeyName} has been created successfuly`)
          }
          setAPIKeyName('')
          setAPIKeyDescription('')
          getAPIKeys()
     }


     const _handleRefreshClick = async (event: React.MouseEvent<HTMLElement>, apiKeyId: number) => {
          event.preventDefault();
          console.log(`API Key ID to refresh => ${apiKeyId}`);
          // Send request to refresh apiKey
          try {
               let refreshApiKey = await requestAPI<IAPIKeyResponse>("api-keys/refresh", {
                    method: "PUT",
                    body: JSON.stringify({
                         endpoint_id: endpoint?.id,
                         api_key_id: apiKeyId,
                         current_user: encodeURIComponent(currentUser)
                    })
               })
               console.log(`Refresh API Key Result => ${JSON.stringify(refreshApiKey, null, 2)}`)
               getAPIKeys()
          } catch (error) {
               console.log(`Error => ${JSON.stringify(error, null, 2)}`)
          }

     }

     const _handleDeleteClick = async (event: React.MouseEvent<HTMLElement>, apiKeyId: number) => {
          event.preventDefault();
          console.log(`API Key ID to delete => ${apiKeyId}`);
          console.log(endpoint);
          // Send Reqest to delete apiKey
          try {
               let deleteApiKey = await requestAPI<any>("api-keys", {
                    method: "DELETE",
                    body: JSON.stringify({
                         endpoint_id: endpoint?.id,
                         api_key_id: apiKeyId,
                         current_user: encodeURIComponent(currentUser)
                    })
               })
               console.log(`Delete API Key Result => ${JSON.stringify(deleteApiKey, null, 2)}`)
               getAPIKeys()
          } catch (error) {
               console.log(`Error => ${JSON.stringify(error, null, 2)}`)
          }
     }

     const handleCopyToClipboard = () => {
          try {
               copyToSystem(adminApiKey as string)
               setSnackbarOpen(true)
          } catch (error) {
               console.log(`Error copying to clipboard => ${JSON.stringify(error, null, 2)}`)
          }
     }

     return (
          <React.Fragment>
               <CssBaseline />
               <NewAPIKeyComponent
                    endp={props}
                    handleSubmit={_handleSubmit}
                    apiKeyNameError={apiKeyNameError}
                    apiKeyDescription={apiKeyDescription}
                    setAPIKeyDescription={setAPIKeyDescription}
                    apiKeyName={apiKeyName}
                    setAPIKeyName={setAPIKeyName}
                    setAPIKeyNameError={setAPIKeyNameError}
               />
               <Grid
                    container
                    spacing={2}
                    direction='row'
                    width={'100%'}
                    marginTop={3}
               >
                    <Grid item width={'100%'}>
                         {apiKeys && apiKeys.length > 0 ? (
                              <Grid
                                   container
                                   spacing={2}
                                   direction="column"
                                   justifyContent="space-between"
                                   alignItems="stretch"
                              >
                                   <Grid item>
                                        <Tooltip title="Your Admin Key for managing your endpoints." placement="bottom-start">
                                             <Typography variant='h6' marginLeft={2}>Your Admin API Key:</Typography>
                                        </Tooltip>
                                   </Grid>
                                   <Grid item>
                                        {/* <Container fixed> */}
                                        <TextField
                                             disabled
                                             variant="outlined"
                                             value={adminApiKey}
                                             fullWidth
                                             InputProps={{
                                                  endAdornment: (
                                                       <InputAdornment position="start">
                                                            <AlignedInputAdornment position="end">
                                                                 <Tooltip title="Copy API Key">
                                                                      <IconButtonWithTooltip role={'button'} onClick={handleCopyToClipboard}>
                                                                           <IoCopyOutline />
                                                                      </IconButtonWithTooltip>
                                                                 </Tooltip>
                                                            </AlignedInputAdornment>
                                                       </InputAdornment>
                                                  ),
                                             }}
                                        />
                                        <Snackbar
                                             open={snackbarOpen}
                                             onClose={() => setSnackbarOpen(false)}
                                             autoHideDuration={2000}
                                             message="Copied to clipboard"
                                        />
                                        {/* </Container> */}
                                   </Grid>
                                   <Grid item>
                                        <Typography variant='h6' marginLeft={2}>Current API Keys:</Typography>
                                   </Grid>
                              </Grid>

                         ) : ''}
                    </Grid>
                    {
                         apiKeys ? (
                              apiKeys.map((apiK, idx) => {
                                   return (
                                        <APIKeyInfoComponent apk={apiK} handleRefreshClick={_handleRefreshClick} handleDeleteClick={_handleDeleteClick} />
                                   )
                              })) : ''
                    }

               </Grid>
          </React.Fragment >
     )
}

export default EndpointAPIKeyComponent;
