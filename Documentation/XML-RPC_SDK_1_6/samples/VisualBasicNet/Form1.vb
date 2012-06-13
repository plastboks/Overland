Imports CookComputing.XmlRpc

Public Interface IsessionLogin
    <CookComputing.XmlRpc.XmlRpcMethod("session_login")> _
    Function session_login(ByVal user As String, ByVal pass As String) _
     As Integer
End Interface

Public Interface IsessionLogout
    <CookComputing.XmlRpc.XmlRpcMethod("session_logout")> _
    Function session_logout(ByVal SessionID As Integer) _
     As Integer
End Interface

Public Interface Iendpoint_sms
    <CookComputing.XmlRpc.XmlRpcMethod("endpoint_sms")> _
    Function endpoint_sms(ByVal sessionID As Integer, ByVal to_ As String, ByVal callback As String, ByVal display As String) _
     As Integer
End Interface

Public Class Form1
    'Private mathProxy As IMath
    Private server As IsessionLogin
    Private server2 As Iendpoint_sms
    Private server3 As IsessionLogout
    Private session As XmlRpcClientProtocol
    Private TxtUrl As String

    Private Sub Btn_Add_Click(ByVal sender As System.Object, _
     ByVal e As System.EventArgs) Handles btnSend.Click

        Try
            server = CType(XmlRpcProxyGen.Create(GetType(IsessionLogin)), IsessionLogin)
            session = CType(server, XmlRpcClientProtocol)
            session.Url = "http://" + txtIP.Text + "/RPC2"
            Dim result1 As Integer = server.session_login("GW-DECT/admin", "ip6000")


            server2 = CType(XmlRpcProxyGen.Create(GetType(Iendpoint_sms)), Iendpoint_sms)
            session = CType(server2, XmlRpcClientProtocol)
            session.Url = "http://" + txtIP.Text + "/RPC2"
            Dim result2 As Integer = server2.endpoint_sms(result1, CInt(txtPhoneNoTo.Text), 0, txtMessage.Text)


            server3 = CType(XmlRpcProxyGen.Create(GetType(IsessionLogout)), IsessionLogout)
            session = CType(server3, XmlRpcClientProtocol)
            session.Url = "http://" + txtIP.Text + "/RPC2"
            Dim result3 As Integer = server3.session_logout(result1)

        Catch ex As Exception
            MsgBox(ex.Message.ToString)
        End Try

    End Sub

End Class
